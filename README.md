# KATO_DB
加藤純一の雑談データセットを作成するプログラムです。  
データセット自体は[kato_db_dataset](https://github.com/konbraphat51/kato_db_dataset)レポジトリに集約させています。

## 全体像

![dLJTJXD15BvlqdVOSEyBbCHmI_GEultQJke6d2N36FymsPc9RO7Ts9JQOY1K2j5ArHAGKB7QXpditnMluCmi1BhQIfoBpPoPSxxpVUUSsPbbQXBwvF5YDfFDK8ik8WFuAV3l84eWtWFx6fmmuAwwpiMllVFXBl0sY07mBl1z40qGJH2VzVv0nrMYtSwAyYSeJqrSb91JweBthlpg88w17y](https://github.com/konbraphat51/kato_db/assets/101827492/fc837d22-c94c-4737-8efe-5ffe6fac97e5)


## 環境導入
このパッケージをcloneし、ここへのパスを通します。データセットはサブモジュールを扱っていますので、管理に留意してください。
```
git clone https://github.com/konbraphat51/kato_db
cd kato_db
conda develop .
git submodule update
```
これに加え、各部門に必要な環境構築があります。各ディレクトリのREADMEに記載しています。