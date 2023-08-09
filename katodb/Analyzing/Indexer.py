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
        titles = self.index_all()
        
        #分解
        self.devide_to_subindex(titles)
        
        #メインスキーマの削除
        self.clear_folder(Consts.transcription_index_folder)
    
    def initialize(self):
        '''
        インデックスファイルの初期化
        '''
        
        #前回のデータを削除する
        self.clear_folder(Consts.transcription_index_folder)
        
        #今回のスキーマ
        self.schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True))
        self.ix_main = create_in(Consts.transcription_index_folder, self.schema)
        
    def clear_folder(self, path):
        '''
        フォルダーのファイルのみをクリアする
        '''
        file_list = os.listdir(path)
        
        for filename in file_list:
            file_path = path + "/" + filename
            if os.path.isfile(file_path):
                os.remove(file_path)
        
    def find_title(self, title):
        '''
        タイトルを完全一致検索する。  
        ヒット内容のリストを返す。
        '''
        
        with self.ix_main.searcher() as searcher:
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
        titles = []
        with self.ix_main.writer() as writer:
            for filename in filenames:
                titles.append(self.update_index(filename, writer))
                
        return titles
        
    def update_index(self, filename, writer):
        '''
        一つのデータのインデックスを作成する。`writer.commit()`すること
        '''
        
        #情報取得
        title, text = self.get_file_info(filename)
        
        #すでに同名のタイトルがあれば、削除する
        # if self.find_title(title) is not None:
        #     self.writer.delete_by_term("title", title)
            
        #インデックス追加
        writer.add_document(title=title, content=text)
        
        return title
    
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
        title = self.convert_title(filename.split("/")[-1].split(".")[0])
            
        #セグメントをスペース区切りで結合
        df_segments = pd.read_csv(filename)
        text = "。".join([str(item) for item in df_segments["text"]])
        
        return title, text
    
    def devide_to_subindex(self, titles):
        '''
        一つあたりのファイルの大きさを抑えるため、サブインデックスを作成
        '''
        
        SINGLE_FILE_N = 300
        
        with self.ix_main.searcher() as searcher:
            for sub_n in range(self.ix_main.doc_count() // SINGLE_FILE_N + 1):
                #フォルダーの作成
                folder_name = Consts.transcription_index_folder + "/sub" + str(sub_n)
                if os.path.exists(folder_name) and os.path.isdir(folder_name):
                    self.clear_folder(folder_name)
                else:
                    os.mkdir(folder_name)
                    
                #サブインデックスの作成
                ix_sub = create_in(folder_name, self.schema)
                with ix_sub.writer() as writer_sub:
                    for doc_n in range(SINGLE_FILE_N * sub_n, min(SINGLE_FILE_N * (sub_n + 1), self.ix_main.doc_count())):
                        document = searcher.search(Term("title", titles[doc_n]))[0]
                        writer_sub.add_document(title=document["title"], content=document["content"])
                ix_sub.close()
    
    def convert_title(self, title):
        return title.replace("-", "m")
    
if __name__ == "__main__":
    indexer = Indexer()
    indexer.run()