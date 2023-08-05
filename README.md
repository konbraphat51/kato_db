# KATO_DB
加藤純一の雑談データセットを作成するプログラムです。  
データセット自体は[kato_db_dataset](https://github.com/konbraphat51/kato_db_dataset)レポジトリに集約させています。

## 環境導入
このパッケージをcloneし、ここへのパスを通します。
```
git clone https://github.com/konbraphat51/kato_db
cd kato_db
conda develop .
```
これに加え、各部門に必要な環境構築があります。各ディレクトリのREADMEに記載しています。

## ファイル形式  

* list_links.csv  
雑談配信のプレイリストのリンク（https://www.youtube.com/playlist?list=PLTklf3SDyrGYJsSNFyruWxwlCfzEORDreのような）を並べる  
year, link  
プレイリストの放送年（不定の場合は空欄に）, プレイリストのURL  
  
* video_links.csv  
動画のリンク。VideoLinkScraperより作成される。  
,date,link,title,length,transcribed  
動画の通し番号, 放送日, 動画URL, 動画の長さ（秒）, 書き起こし済みフラグ  
書き起こし済みフラグは下記の番号が与えられる：  
    * -1: 未書き起こし
    * 0: tinyモデルによる書き起こし
    * 1: baseモデルによる書き起こし
    * 2: mediumモデルによる書き起こし
    * 3: large-v2モデルによる書き起こし