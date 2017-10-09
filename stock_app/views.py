from django.http import HttpResponse
from django.shortcuts import render
import configparser
import quandl
import datetime
from pprint import pprint

from stock_app.models import DailyData


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
