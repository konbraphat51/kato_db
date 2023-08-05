import MeCab
import pandas as pd
import os
import re
from katodb import Consts, Utils
from joblib import Parallel, delayed
import gc

class Tokenizer:
    '''
    書き起こしデータをTFIDFで解析し、キーワードを抽出し、そのキーワードにスコア付けを行うクラス
    '''
    
    def run(self):
        filenames = self.get_files()
        Parallel(n_jobs=-4, verbose=10)([delayed(self.process)(filename) for filename in filenames])
    
    def get_files(self):
        '''
        書き起こしデータのファイル名取得
        '''
        folder = Consts.trascription_raw_folder
        filenames = os.listdir(folder)
        
        #「数字-数字.csv」のパターンを抽出
        pattern = r"\d+-\d+\.csv"
        filenames = [filename for filename in filenames if re.match(pattern, filename)]

        return [folder + "/" + filename for filename in filenames]
    
    def process(self, filename):
        '''
        ファイル名から形態素解析を行い、保存する。（並列処理用）
        '''
        gc.collect()
        
        title, segments = self.get_file_info(filename)
        self.tokenize(segments, Consts.transcription_tokenized_folder + "/" + title + ".csv")
    
    def get_file_info(self, filename):
        '''
        ファイル名から(タイトル, セグメントリスト)を取得
        '''
    
        #インデックスを取得
        title = filename.split("/")[-1].split(".")[0]
            
        #セグメントをスペース区切りで結合
        df_segments = pd.read_csv(filename)
        segments = list(df_segments["text"])
        
        return title, segments
    
    def tokenize(self, segments, filename):
        '''
        書き起こしデータを形態素解析。結果は`filename`に保存される。
        '''
        
        #本関数の返り値にまとめて形態素情報を返そうとすると、メモリサイズが膨大になるので、逐次ファイルに保存する必要がある。
        
        #ファイルの用意
        with open(filename, "w", encoding="utf-8") as f:
            pass
        
        tagger = MeCab.Tagger(Consts.mecab_params)
        first = True
        for segment in segments:
            #セグメント間には「*, BOS/EOS」が挟まれるので、こちらから区切りを入れる必要はない
                        
            nodes = tagger.parseToNode(segment)
            
            while nodes:
                sp = nodes.feature.split(",")
                
                #品詞
                pos = sp[0]
                
                #書字形基本形
                if len(sp) > 10:
                    original = sp[10]
                else:
                    #原形がない場合は表層形を代わりに使う
                    original = nodes.surface
            
                #記録
                self.write_token(original, pos, filename)
                
                #これがないと無限ループ
                nodes = nodes.next
        
    def write_token(self, original, pos, filename):
        '''
        `filename`に形態素情報1つ分を追加で書き込む
        '''
        
        with open(filename, "a", encoding="utf-8") as f:
            f.write(original + "," + pos + "\n")
        
if __name__ == "__main__":
    breaker = Tokenizer()
    breaker.run()
    #breaker.process("Data/Transcription_raw/15-4.csv")    