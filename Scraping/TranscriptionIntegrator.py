import pandas as pd
import os
import re

'''
生成された書き起こし進捗をvideo_links.csvに反映する
'''
class TranscriptionIntegrator:
    def run(self):
        df_video_links = pd.read_csv("Data/video_links.csv", index_col=0)
        
        #いったん全て-1（未実施）にする
        df_video_links["transcribed"] = -1
        
        #進捗に応じて記録
        transcribed = self.get_transcribed()
        for index, model in transcribed:
            if model > df_video_links.at[index, "transcribed"]:
                df_video_links.at[index, "transcribed"] = model
                
        df_video_links.to_csv("Data/video_links.csv")

    '''
    (書き起こされたファイルのインデックス, モデル番号)のリストを返す
    '''    
    def get_transcribed(self):
        file_names = []
        folder_path = "Data/Transcription_raw"
        
        pattern = r"\d+-\d+\.csv"  # 「数字-数字.csv」のパターン

        for filename in os.listdir(folder_path):
            if re.match(pattern, filename):
                file_names.append(filename)

        transcribed = []
        for filename in file_names:
            sp = filename.split("-")
            index = int(sp[0])
            model = int(sp[1].split(".")[0])
            transcribed.append((index, model))

        return transcribed
    
if __name__ == "__main__":
    integrator = TranscriptionIntegrator()
    integrator.run()