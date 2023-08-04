
class Consts:
    '''
    定数まとめ
    '''
    
    #要編集（ご自分の環境に合わせて）
    mecab_params = '-u "C:/Program Files/MeCab/dic/NEologd.dic"'
    nico_pass = "katodb/Utils/nico_pass.txt"
    
    #多分編集しない
    list_links_file = "Data/list_links.csv"
    video_links_file = "Data/video_links.csv"
    trascription_raw_folder = "Data/Transcription_raw"
    keywords_folder = "Data/Keywords"
    transcription_tokenized_folder = "Data/Transcription_tokenized"
    
    def nico_account():
        '''
        ニコニコ動画のアカウント情報（メアド、パスワード）を返す
        '''
        
        with open(Consts.nico_pass,  "r") as f:
            email, password = f.read().split()
        return (email, password)