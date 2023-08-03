import MeCab
import pandas as pd
import os
import re
from .. import Consts
from joblib import Parallel, delayed


class Tokenizer:
    '''
    書き起こしデータをTFIDFで解析し、キーワードを抽出し、そのキーワードにスコア付けを行うクラス
    '''
    def run(self):
        filenames = self.get_files()
        Parallel(n_jobs=-1, verbose=10)([delayed(self.process)(filename) for filename in filenames])
    
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
        title, text = self.get_file_info(filename)
        tokens = self.tokenize(text)
        self.save_tokenized(title, tokens)
    
    def get_file_info(self, filename):
        '''
        ファイル名から(タイトル, 書き起こしテキストを1文字列に集約)を取得
        '''
    
        #インデックスを取得
        title = filename.split(".")[0]
            
        #セグメントをスペース区切りで結合
        df_segments = pd.read_csv(filename)
        texts_this = df_segments["text"]
        text = ".".join(texts_this)
        
        return title, text
    
    def tokenize(self, text):
        '''
        書き起こしデータを形態素解析
        [(原形, 品詞)]を返す
        '''
        
        tagger = MeCab.Tagger(Consts.mecab_params)
        nodes = tagger.parseToNode(text)
        
        tokens = []
        
        while nodes:
            sp = nodes.feature.split(",")
            
            #品詞
            pos = sp[0]
            
            #原形
            if len(sp) > 6:
                original = sp[6]
            else:
                #原形がない場合は表層形を代わりに使う
                original = nodes.surface
        
            token = (original, pos)
            
            tokens.append(token)
            
        return tokens
    
    def save_tokenized(self, title, tokens):
        '''
        分解されたデータを保存する
        '''
    
        filename = Consts.transcription_tokenized_folder + "/" + title + ".csv"
        
        df = pd.DataFrame(tokens, columns=["original", "pos"])
        df.to_csv(filename)
        
        
if __name__ == "__main__":

    breaker = Tokenizer()
    breaker.get_texts()
        