from whoosh.index import create_in
from whoosh.fields import *
from whoosh.query import *
from whoosh.qparser import QueryParser
from katodb import Consts
import os
import pandas as pd

class Indexer:
    '''
    検索用のインデックスファイルを作成するクラス
    '''
    
    def run(self):
        self.initialize()
        self.index_all()
    
    def initialize(self):
        '''
        インデックスファイルの初期化
        '''
        
        #前回のデータを削除する
        self.clear_folder()
        
        #今回のスキーマ
        schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True))
        ix = create_in(Consts.transcription_index_folder, schema)
        self.writer = ix.writer()
        
    def clear_folder(self):
        '''
        スキーマのあるフォルダーをクリアする
        '''
        file_list = os.listdir(Consts.transcription_index_folder)
        
        for filename in file_list:
            os.remove(Consts.transcription_index_folder + "/" + filename)
        
    def find_title(self, title):
        '''
        タイトルを完全一致検索する。  
        ヒット内容のリストを返す。
        '''
        
        with self.writer.searcher() as searcher:
            query = Term("title", title)
            results = searcher.search(query)
            
        if len(results) > 0:
            return results[0]
        else:
            return None
    
    def index_all(self):
        '''
        Dataにある全ての書き起こしデータをインデックスする。
        '''
        
        filenames = self.get_files()
        for filename in filenames:
            self.update_index(filename)
            
        self.writer.commit()
        
    def update_index(self, filename):
        '''
        一つのデータのインデックスを作成する。`self.writer.commit()`すること
        '''
        
        #情報取得
        title, text = self.get_file_info(filename)
        
        #すでに同名のタイトルがあれば、削除する
        # if self.find_title(title) is not None:
        #     self.writer.delete_by_term("title", title)
            
        #インデックス追加
        self.writer.add_document(title=title, content=text)
    
    def get_files(self):
        '''
        書き起こしデータのファイル名取得
        '''
        
        folder = Consts.transcription_raw_folder
        filenames = os.listdir(folder)
        
        #「数字-数字.csv」のパターンを抽出
        pattern = r"\d+-\d+\.csv"
        filenames = [filename for filename in filenames if re.match(pattern, filename)]

        return [folder + "/" + filename for filename in filenames]
    
    def get_file_info(self, filename):
        '''
        ファイル名から(タイトル, セグメントリスト)を取得
        '''
    
        #インデックスを取得
        title = filename.split("/")[-1].split(".")[0]
            
        #セグメントをスペース区切りで結合
        df_segments = pd.read_csv(filename)
        text = "。".join([str(item) for item in df_segments["text"]])
        
        return title, text
    
if __name__ == "__main__":
    indexer = Indexer()
    indexer.run()