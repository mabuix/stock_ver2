from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
import configparser
import quandl
import datetime
from pprint import pprint
from stock_app.models import DailyData
from stock_app.models import Fundamentals_Data
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def index(request):
    return HttpResponse("Hello, world. You're at the stock_apps index.")


def get_latest_data(code):
    """既にDBに保存されている最新のデータを取得"""
    latest_data = DailyData.objects.filter(code=code).order_by('-date').first()
    return latest_data


def get_daily_data(request):
    """外部サイト(quandl)から、日足データ取得"""

    conf = configparser.ConfigParser()
    conf.read('config.ini')
    api_key = conf.get('quandl', 'api_key')
    quandl.ApiConfig.api_key = api_key

    # DB保存用リスト
    result_list = []

    # 読み込み専用でcode.txtを開く
    with open('code.txt', 'r') as codes:
        for code in codes:
            # 改行を削除
            code = code.rstrip()

            # DBから最新のデータを取得
            latest_data = get_latest_data(code)

            if latest_data is None:
                # 初めてデータを取得する銘柄の場合は、過去分全てのデータを取得する
                query_result_list = quandl.get('TSE/' + code, returns="numpy")
            elif latest_data.date >= datetime.date.today():
                # 本日取得済みなら、処理をスキップする
                continue
            else:
                # latest_dataの翌日から、データ取得
                next_day = latest_data.date + datetime.timedelta(days=1)
                query_result_list = quandl.get('TSE/' + code, start_date=next_day, returns="numpy")

            daily_data_list = []
            for query_result in query_result_list:
                date, open_p, high, low, close, volume = query_result
                daily_data = DailyData.objects.create_daily_data(code, date, open_p, high, low, close, volume)
                daily_data_list.append(daily_data)

            # 取得したデータをDB保存用リストに詰める
            result_list.extend(daily_data_list)

    # 取得したデータリストを、DBにバルクインサート
    DailyData.objects.bulk_create(result_list)

    return HttpResponse("metrics get.")


def get_fundamental_data(request):
    """外部サイト()から、基礎的データ取得"""

    # TODO: DBに入れるデータ、銘柄コード(PK)、銘柄名、発行済株式数

    return HttpResponse("metrics get.")


def get_daily_data_bak(request):
    """外部サイト(quandl)から、日足データ取得"""

    conf = configparser.ConfigParser()
    conf.read('config.ini')
    api_key = conf.get('quandl', 'api_key')

    quandl.ApiConfig.api_key = api_key
    code = '3990'
    result = quandl.get('TSE/' + code, start_date='2017-09-11', end_date='2017-09-11', returns="numpy")
    date = result[0]['Date']
    open = result[0]['Open']
    high = result[0]['High']
    low = result[0]['Low']
    close = result[0]['Close']
    volume = result[0]['Volume']

    # Debug
    print(code)
    print(date)
    print(open)
    print(high)
    print(low)
    print(close)
    print(volume)

    # 日足のインスタンス生成
    daily_data = DailyData.objects.create_daily_data(code, date, open, high, low, close, volume)
    # DBに保存
    daily_data.save()

    return HttpResponse("metrics get.")


def create_spreadsheet_data(request):
    """
    google spreadsheetにデータ作成

    スプレッドシート操作用に作成したGoogle APIsプロジェクトのユーザーを、操作したいシートに権限追加して使用する。
    ユーザー情報は、発行されたService Account Key内の、client_emailに記載。
    % cat /Users/manatonakane/git/stock_ver2/sandbox-a739dfc2f0da.json
    """

    scope = ['https://spreadsheets.google.com/feeds']

    # 発行されたService Account Key(jsonファイル)を指定する
    credentials = ServiceAccountCredentials.from_json_keyfile_name('sandbox-a739dfc2f0da.json', scope)

    gc = gspread.authorize(credentials)

    # ワークブックを開く
    workbook = gc.open("投資銘柄管理シート for python")

    # シート名を指定して開く
    try:
        worksheet = workbook.worksheet("data")
        # 開けたら、内容リセットするためワークシートを削除
        workbook.del_worksheet(worksheet)
    except gspread.exceptions.WorksheetNotFound:
        pass

    # ワークシートを作成
    worksheet = workbook.add_worksheet(title="data", rows="100", cols="20")

    # セルのヘッダー更新
    worksheet.update_acell('A1', 'コード')
    worksheet.update_acell('B1', '名称')
    worksheet.update_acell('C1', '日時')
    worksheet.update_acell('D1', '株価')
    worksheet.update_acell('E1', '時価総額(百万円)')
    worksheet.update_acell('F1', '発行済株式数')

    codes = []
    # 読み込み専用でcode.txtを開く
    with open('code.txt', 'r') as texts:
        for text in texts:
            # 改行を削除
            codes.append(text.rstrip())

    fundamentals_data_list = Fundamentals_Data.objects.filter(code__in=codes)
    que_list = []
    for data in fundamentals_data_list:
        daily_data = DailyData.objects.filter(code=data.code).order_by('-date').first()
        que_list.append(data.code)
        que_list.append(data.name)
        que_list.append(daily_data.date)
        que_list.append(daily_data.close)
        que_list.append(data.market_capitalization)
        que_list.append(data.outstanding_shares)

    # セルの範囲指定(セルの行数 = ヘッダー一行 + 銘柄数)
    row_count = fundamentals_data_list.count() + 1
    cell_list = worksheet.range('A2:F' + str(row_count))

    for cell in cell_list:
        cell.value = que_list.pop(0)

    # バッチ更新
    worksheet.update_cells(cell_list)

    return HttpResponse("data created.")