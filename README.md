# pythonで銘柄監視プログラム作成 ver2

## ver2の方向性、達成したいこと
  - まずは最速、最低限で形にする
  - 無料
    - 全てローカルで完結するように作る。
  - 今後の資材に
    - glthubにソースを上げるところまでやって、今後使いまわせるように。

## ver2 仕様
  - quandlから指定銘柄の時系列データを取得
    https://www.quandl.com/data/TSE-Tokyo-Stock-Exchange/usage/quickstart/python
  - 取得した銘柄のデータを保持
  - スプレッドシートに下記項目を出力
    - 銘柄コード
    - 銘柄名
    - 現在株価
    - 時価総額(百万円) 

## 技術選定
  - 言語
    - python
  - フレームワーク
    - Django
  - データベース
    - MySQL

## 使い方
- 取得したい銘柄の銘柄コードをcode.txtに記述
```
% cat /Users/manatonakane/git/stock_ver2/code.txt                                         [19:03:36]
6094
6531
3921
```

- 日足の時系列データをDBに保存
```
# djangoの開発用サーバーを起動
% /Users/manatonakane/git/stock_ver2/manage.py runserver                                  [19:03:52]
Performing system checks...

System check identified no issues (0 silenced).
October 06, 2017 - 19:06:56
Django version 1.11.5, using settings 'stock_ver2.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
```
# ブラウザからapiにアクセスで処理実行
http://127.0.0.1:8000/stock_app/get_daily_data/
```

- ファンダメンタル情報をDBに保存(scrapyでスクレイピング起動)
```
% pwd                                                                                     [16:28:48]
/Users/manatonakane/git/stock_ver2/stock_app/stock_crawl
% scrapy crawl fundamentals_crawl                                                         [16:34:46]
```

- 株価データをgoogle spreadsheetに出力
```
http://127.0.0.1:8000/stock_app/create_spreadsheet_data/
```