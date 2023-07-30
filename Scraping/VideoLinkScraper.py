from pytube import Playlist, YouTube
import pandas as pd
from tqdm import tqdm
from joblib import Parallel, delayed

'''
list_links.csvからスクレイピングするべき動画のリンクの一覧video_links.csvを作成する。
'''
class VideoLinkScraper:
    def run(self):
        df_list_links = self.get_lists()
        df_video_links = self.get_videos_from_links(df_list_links)
        self.save_video_links(df_video_links)
    
    '''list_links.csvからプレイリストのリンクを取得する。'''
    def get_lists(self):
        return pd.read_csv('Scraping/list_links.csv')
    
    '''プレイリストのリンクから動画のリンクを取得する。'''
    def get_videos_from_links(self, df_list_links):
        output = Parallel(n_jobs=-1, verbose=10)([delayed(self.get_videos_from_link)(row) for _, row in df_list_links.iterrows()])

        video_links = []
        for links in output:
            for content in links:
                video_links.append(content)
     
        df_video_links = pd.DataFrame(video_links, columns=['date', 'link', 'title', "length"])
        
        return df_video_links
    
    def get_videos_from_link(self, row):
        video_links = []
        playlist = Playlist(row['link'])
        for video_link in tqdm(playlist.video_urls):
            video = YouTube(video_link)
            video_links.append([video.publish_date, video_link, video.title, video.length])
        
        return video_links
    
    def save_video_links(self, df_video_links):
        df_video_links.to_csv('Scraping/video_links.csv', index=False)

if __name__ == '__main__':
    scraper = VideoLinkScraper()
    scraper.run()