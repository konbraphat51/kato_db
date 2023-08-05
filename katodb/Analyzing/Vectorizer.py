import os
import re
from katodb import Consts, Utils

class Vectorizer:
    '''
    形態素解析データをもとに、TF-IDFベクトル、Countベクトルを計算するクラス
    '''
    
    def run(self):
        filenames = self.get_files()
        texts = self.get_texts(filenames)
    
    def get_files(self):
        '''
        形態素解析データのファイル名取得
        '''
        
        folder = Consts.transcription_tokenized_folder
        filenames = os.listdir(folder)
        
        #「数字-数字.csv」のパターンを抽出
        pattern = r"\d+-\d+\.csv"
        filenames = [filename for filename in filenames if re.match(pattern, filename)]

        return [folder + "/" + filename for filename in filenames]
    
    def get_text(self, filename):
        '''
        一つのファイルから形態素解析データを取得
        '''
        
        with open(filename, "r") as f:
            text = f.read()
            
        return text
    
    def get_texts(self, filenames):
        '''
        全ファイルから形態素データを取得。リストの一つの要素が一つの文書を表す
        '''
        
        return [self.get_text(filename) for filename in filenames]