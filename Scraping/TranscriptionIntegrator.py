import pandas as pd
import os
import re
from .. import Consts

class TranscriptionIntegrator:
    '''
    生成された書き起こし進捗をvideo_links.csvに反映する
    '''

    def run(self):
        df_video_links = pd.read_csv(Consts.video_links_file, index_col=0)
        
        #いったん全て-1（未実施）にする
        df_video_links["transcribed"] = -1
        
        #進捗に応じて記録
        transcribed = self.get_transcribed()
        for index, model in transcribed:
            if model > df_video_links.at[index, "transcribed"]:
                df_video_links.at[index, "transcribed"] = model
                
        df_video_links.to_csv(Consts.video_links_file)

    def get_transcribed(self):
        '''
        (書き起こされたファイルのインデックス, モデル番号)のリストを返す
        '''    
        file_names = []
        folder_path = Consts.trascription_raw_folder
        
        pattern = r"\d+-\d+\.csv"  # 「数字-数字.csv」のパターン

        for filename in os.listdir(folder_path):
            if re.match(pattern, filename):
                file_names.append(filename)

        transcribed = []
        for filename in file_names:
            sp = filename.split("-")
            index = int(sp[0])
            model = int(sp[1].split(".")[0])
            transcribed.append((index, model))

        return transcribed
    
if __name__ == "__main__":
    integrator = TranscriptionIntegrator()
    integrator.run()