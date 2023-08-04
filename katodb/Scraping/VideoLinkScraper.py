from pytube import Playlist, YouTube
from niconico import NicoNico
import pandas as pd
from joblib import Parallel, delayed
import re
from datetime import datetime
import os
if __name__ == "__main__":
    from katodb import Consts, Utils
else:
    from ..Utils import Consts, Utils


class VideoLinkScraper:
    '''
    list_links.csvからスクレイピングするべき動画のリンクの一覧video_links.csvを作成する。
    '''

    def __init__(self):
        self.niconico_client = NicoNico()
    
    def run(self):
        df_list_links = self.get_lists()
        df_video_links = self.get_current_videos()
        df_video_links = self.get_videos_from_links(df_list_links, df_video_links)
        self.save_video_links(df_video_links)
    
    def get_lists(self):
        '''list_links.csvからプレイリストのリンクを取得する。'''
        return pd.read_csv(Consts.list_links_file)
    
    def get_current_videos(self):
        '''現時点での取得済みリンクのデータフレームを取得する。なければ空'''
        if os.path.isfile(Consts.video_links_file):
            return pd.read_csv(Consts.video_links_file, index_col=0)
        else:
            return pd.DataFrame(columns=['date', 'link', 'title', "length", "transcribed"])
    
    
    def get_videos_from_links(self, df_list_links, df_video_links):
        '''プレイリストのリンクから動画のリンクを取得する。'''
        
        current_links = set(df_video_links["link"])
        
        #Youtubeを処理
        output = Parallel(n_jobs=-1, verbose=10)([delayed(self.get_videos_from_link_youtube)(row, current_links) for _, row in df_list_links[df_list_links["link"].str.contains("youtube")].iterrows()])
        #output = [self.get_videos_from_link_youtube(row) for _, row in df_list_links[df_list_links["link"].str.contains("youtube")].iterrows()]
        video_links = []
        for links in output:
            for content in links:
                video_links.append(content)
                    
        df_temp = pd.DataFrame(video_links, columns=['date', 'link', 'title', "length", "transcribed"])
        df_video_links = pd.concat([df_video_links, df_temp])        
        
        #ニコニコ動画を処理
        output = Parallel(n_jobs=-1, verbose=10)([delayed(self.get_videos_from_link_niconico)(row, current_links) for _, row in df_list_links[df_list_links["link"].str.contains("nicovideo")].iterrows()])
        #output = [self.get_videos_from_link_niconico(row) for _, row in df_list_links[df_list_links["link"].str.contains("nicovideo")].iterrows()]
        video_links = []
        for links in output:
            for content in links:
                video_links.append(content)
                
        df_temp = pd.DataFrame(video_links, columns=['date', 'link', 'title', "length", "transcribed"])
        df_video_links = pd.concat([df_video_links, df_temp])

        return df_video_links
    
    def get_videos_from_link_youtube(self, row, got_links):
        video_links = []
        playlist = Playlist(row['link'])
        for video_link in playlist.video_urls:
            if video_link in got_links:
                #すでに取得済み
                continue
            video = YouTube(video_link)
            date = self.get_date(video.title, video.description, video.publish_date)
            video_links.append([date, video_link, video.title.replace(",", ""), video.length, -1])
        
        return video_links
    
    def get_videos_from_link_niconico(self, row, got_links):
        video_links = []
        mylists = self.niconico_client.video.get_mylist(row['link'])
    
        for mylist in mylists:
            for mylist_item in mylist.items:
                link = mylist_item.video.url
                if link in got_links:
                    #すでに取得済み
                    continue
                try:
                    video = mylist_item.video.get_video().__data__["video"]
                    date = self.get_date(video["title"], video["description"], datetime.fromisoformat(video["registeredAt"]))
                    video_links.append([date, link, video["title"], video["duration"], -1])
                except:
                    #削除済みの動画
                    pass

        return video_links
    
    def get_date(self, title, description, publish_date):
        '''
        概要欄から日付を取得する。
        「MMMM/MM/DD」の文字列形式で返す
        '''
        #複数の正規表現で日付を抽出
        for re_pattern, datetime_pattern in [(r"\b(\d{4})/(\d{1,2})/(\d{1,2})\b", "%Y/%m/%d"), (r"\b(\d{4})年(\d{1,2})月(\d{1,2})日\b", "%Y年%m月%d日"), (r"\b\d{8}\b", "%Y%m%d")]:        
            #タイトルについて
            matched = re.search(re_pattern, title)
            if matched:
                #タイトルに該当あり
                date = datetime.strptime(matched.group(0), datetime_pattern)
                break
            
            #概要欄について
            if description is str:
                matched = re.search(re_pattern, description)
                if matched:
                    date = datetime.strptime(matched.group(0), datetime_pattern)
                    break
        else:
            date = publish_date
    
        return date.strftime("%Y/%m/%d")
    
    def save_video_links(self, df_video_links):
        df_video_links.to_csv(Consts.video_links_file)

if __name__ == '__main__':
    scraper = VideoLinkScraper()
    scraper.run()