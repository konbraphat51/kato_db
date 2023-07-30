# スクレイピング部
まずlist_links.csvをセット  

（初回時）VideoLinkScraper.pyにより動画一覧video_links.csvを作成  
  
（GPUがない場合）Transcriver_colab.ipynbをGoogle colabに読み込ませ、書き起こし開始（数日単位で時間がかかる）
  
やること  
* 後続の動画をvideo_links.csvに動的に追加する機能  
  
ファイル形式  

list_links.csv  
雑談配信のプレイリストのリンク（https://www.youtube.com/playlist?list=PLTklf3SDyrGYJsSNFyruWxwlCfzEORDreのような）を並べる  
year, link  
プレイリストの放送年（不定の場合は空欄に）, プレイリストのURL  
  
video_links.csv  
動画のリンク。VideoLinkScraperより作成される。  
,date,link,title,length,transcribed  
動画の通し番号, 放送日, 動画URL, 動画の長さ（秒）, 書き起こし済みフラグ  
書き起こし済みフラグは下記の番号が与えられる：  
* -1: 未書き起こし
* 0: tinyモデルによる書き起こし
* 1: baseモデルによる書き起こし
* 2: mediumモデルによる書き起こし
* 3: largeモデルによる書き起こし