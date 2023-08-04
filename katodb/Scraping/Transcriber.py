#import whisper
from faster_whisper import WhisperModel
from pytube import YouTube, Channel
from niconico import NicoNico
import pandas as pd
from random import shuffle, randint
import concurrent.futures as cf
import os
from tqdm import tqdm
import gc

if __name__ == "__main__":
    from katodb import Consts, Utils
else:
    from ..Utils import Consts, Utils

class Transcriber:
    '''
    video_links.csvから書き起こしを行うクラス
    '''

    #番号とモデル名の対応
    model_num_to_name = {
        -1: "none",
        0: "tiny",
        1: "base",
        2: "small",
        3: "medium",
        4: "large-v2"
    }

    def __init__(self, model = 4):
        self.df_videos = pd.read_csv(Consts.video_links_file)
        self.model = model 
        
        #whisperモデルの読み込み
        self.whisper_model = WhisperModel(Transcriber.model_num_to_name[model], device="cuda", compute_type="float16")

    def run(self, mode = 0):
        '''
        作動する。途中中断しても進捗は保存される。
        mode
        0->未書き起こしを対象に
        1->改善対象（モデルが下位のもの）を対象に
        '''
        
        if mode == 0:
            index_target = self.get_untranscribeds()
        elif mode == 1:
            index_target = self.get_improvables()

        #with cf.ThreadPoolExecutor(max_workers=2) as executor:
        with cf.ProcessPoolExecutor(max_workers=2) as executor:
            futures = []
            for index in index_target:
                row = self.df_videos.iloc[index]
                futures.append(executor.submit(self.transcribe, index, row["link"], self.model))

            _ = cf.as_completed(futures)
                
    def get_untranscribeds(self):
        '''
        未書き起こしの動画のインデックス一覧を取得。一覧はシャッフルされている
        '''
        index_untranscribed = list(self.df_videos[self.df_videos["transcribed"] == -1].index)
        shuffle(index_untranscribed)
        return index_untranscribed

    def get_improvables(self):
        '''
        self.modelの方が上位のデータのインデックス一覧を取得。一覧はシャッフルされる。
        '''
        index_improvable = list(self.df_videos[self.df_videos["transcribed"] < self.model].index)
        shuffle(index_improvable)
        return index_improvable

    def transcribe(self, index, link, model):
        '''
        書き起こしを行う。書き起こしファイルの保存、video_links.csvの更新も行われる
        '''
        Utils.time_print("start: " + str(index))

        #動画をダウンロード
        audio_file_name = str(index) + ".mp4"
        self.download_video(link, audio_file_name)

        Utils.time_print("downloaded: " + str(index))

        #書き起こし
        #transcription = self.whisper_model.transcribe(audio_file, language = "ja")["segments"]
        segments, _ = self.whisper_model.transcribe(audio_file_name, language="ja")

        #データ整理
        transcription = []
        for segment in segments:
            transcription.append([segment.start, segment.end, segment.text])

        #ダウンロードした動画を削除（容量のため）
        os.remove(audio_file_name)

        #書き起こしファイルの保存
        transcription_file_name = Consts.trascription_raw_folder + "/" + str(index) + "-" + str(model) + ".csv"
        df_transcription = pd.DataFrame(data=transcription, columns=['start', 'end', 'text'])
        df_transcription.to_csv(transcription_file_name, index = False)

        Utils.time_print("transcribed: " + str(index))

        gc.collect()
        return index

    def download_video(self, link, file_name):
        if "youtube" in link:
            YouTube(link).streams.filter(only_audio=True).first().download(filename=file_name)
        elif "nicovideo" in link:
            client = NicoNico()
            with open(Consts.nico_pass, "r") as f:
                email, password = f.read().split()
            client.login(client, email, password)
            with client.video.get_video(link) as video:
                video.download(file_name)