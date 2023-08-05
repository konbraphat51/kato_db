import os
import re
import pandas as pd
from katodb import Consts, Utils
from katodb.Analyzing.rake_ja import JapaneseRake, Tokenizer

class KeywordSetter:
    '''
    書き起こしデータをもとに配信のキーワードを設定する。
    '''
    
    def run(self):
        filenames = self.get_files()
        for filename in filenames:
            keywords = self.get_keywords_from_file(filename)
            #TODO: このあと
    
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
    
    def get_keywords_from_file(self, filename):
        '''
        一つのファイルをまとめてキーワード抽出。  
        `get_text`と`get_keywords`をまとめて実行する。
        '''
        
        return self.get_keywords(self.get_text(filename))
    
    def get_text(self, filename):
        '''
        書き起こしデータを一つのテキストにまとめる
        '''
        
        df = pd.read_csv(filename)
            
        texts = df["text"]
        
        text = ". ".join(texts)
        
        return text
    
    def get_keywords(self, text):
        '''
        キーフレーズ抽出。
        (キーワード, スコア)のリストを返す。
        '''
        
        rake = JapaneseRake(max_length=3)
        tokens = Tokenizer(rawargs=Consts.mecab_params).tokenize(text)
        
        rake.extract_keywords_from_text(tokens)
        keywords = rake.get_ranked_phrases_with_scores()
        
        return [(x[1], x[0]) for x in keywords]
    
if __name__ == "__main__":
    KeywordSetter().run()