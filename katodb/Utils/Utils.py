from datetime import datetime

class Utils:
    '''
    ヘルパークラス
    '''
    
    def time_print(text):
        '''
        時間とともにテキストを表示する
        '''
        current_time = datetime.now()
        print(f"[{current_time.strftime('%H:%M:%S')}]: {text}")