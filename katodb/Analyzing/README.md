# 分析部

## 環境
MeCabが必要となります。（0.996.2の動作を確認しています）  
導入：https://qiita.com/probabilityhill/items/e60831380173f408ac5d  
ナウい単語を認識するため、一番新しい[Unidict](https://clrd.ninjal.ac.jp/unidic/back_number.html)を使用します。  
最新の「話し言葉」のFullをダウンロードして、下記の操作で加藤純一用語（「はんぜう」など）を取り込みます。

```
cd C:\Program Files\MeCab\bin

mecab-dict-index -d "unidicフォルダーのパス" -u "C:\Program Files\MeCab\dic\unidic_kato.dic" -f utf-8 -t utf-8 "dictionary_adding.csvへのパス"
```