from whoosh.index import create_in
from whoosh.fields import *
from katodb import Consts

class Indexer:
    '''
    検索用のインデックスファイルを作成するクラス
    '''
    
    def initialize(self):
        '''
        インデックスファイルの初期化
        '''
        
        schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True), content=KEYWORD)
        ix = create_in(Consts.transcription_index_folder, schema)
        self.writer = ix.writer()
        
        