from VideoLinkScraper import VideoLinkScraper
from TranscriptionIntegrator import TranscriptionIntegrator
from Transcriber import Transcriber
from katodb import Consts, Utils

class Scraper:
    '''
    スクレピング部処理を一本化するクラス。  
    `Transcriber`が長いため、途中で打ち止めても問題ない
    '''
    
    def run(has_gpu = False):
        '''
        全処理まとめて行う。
        GPU環境がない場合は、has_gpuをFalseにしないとエラーが出る。Falseにした場合は打ち止めにする。
        '''
        
        Utils.time_print("start: 動画ＵＲＬの収集")
        VideoLinkScraper().run()
        Utils.time_print("end: 動画ＵＲＬの収集")
        
        Utils.time_print("start: 現状の書き起こし状況の取得")
        TranscriptionIntegrator().run()
        Utils.time_print("end: 現状の書き起こし状況の取得")
        
        if has_gpu:
            Utils.time_print("start: 書き起こし")
            Transcriber(model=4).run(mode=0)
            Utils.time_print("end: 書き起こし")
            
            #最終的なvideo_links.csvの更新
            Utils.time_print("start: 現状の書き起こし状況の取得")
            TranscriptionIntegrator().run()
            Utils.time_print("end: 現状の書き起こし状況の取得")
            
        else:
            print("GPU環境がないため、打ち止めます。Transcriber_colab.ipynbを実行してください。")