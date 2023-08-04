# スクレイピング部
データを用意するパートです。

※large-v2モデルでは新語の対応ができていない可能性がありますので、別途日本語ファインチューニングされた新しくて優れたモデルを探しています。データ量が膨大なのでfaster_whisperに対応したものを。

## 手順
* まずlist_links.csvをセット  
雑談動画のプレイリストを記入すると、それを取得する。  

* `VideoLinkScraper`により動画一覧video_links.csvを作成  
  
* （GPUがない場合）Transcriver_colab.ipynbをGoogle colabに読み込ませて動かす。（詳細はnotebookに記載）（GPU制限頻繁にかかる）

* (GPUがある場合) `Transcriber`を稼働させる。

これで動画の書き起こしデータが`Data/Transcription_raw`に記録されます。
  
  
## 環境
faster_whisperのために、CUDA 11.x (12.x非対応)、cuDNN 8.xが必要となります。  
導入はこちらがわかりやすいです：https://qiita.com/TrashBoxx/items/2e884998cd1193f73e2f