
class Consts:
    '''
    定数まとめ
    '''
    
    #要編集（ご自分の環境に合わせて）
    ##-r (mecabrcのパス) -u (辞書のパス)を指定
    mecab_params = '-r "C:/Program Files/MeCab/etc/mecabrc" -u "C:/Program Files/MeCab/dic/unidic_kato.dic"'
    
    ##ニコ動のアカウント情報
    nico_pass = "katodb/Utils/nico_pass.txt"
    
    #多分編集しない
    list_links_file = "Data/list_links.csv"
    video_links_file = "Data/video_links.csv"
    transcription_raw_folder = "Data/Transcription_raw"
    keywords_folder = "Data/Keywords"
    transcription_tokenized_folder = "Data/Transcription_tokenized"
    transcription_index_folder = "Data/Transcription_index"
    scraping_cache_folder = "katodb/Scraping/cache"
    
    def nico_account():
        '''
        ニコニコ動画のアカウント情報（メアド、パスワード）を返す
        '''
        
        with open(Consts.nico_pass,  "r") as f:
            email, password = f.read().split()
        return (email, password)