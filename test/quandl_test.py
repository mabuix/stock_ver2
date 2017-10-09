import configparser
import quandl
import datetime
from pprint import pprint

def get_daily_data_test():
    conf = configparser.ConfigParser()
    conf.read('../config.ini')
    api_key = conf.get('quandl', 'api_key')

    quandl.ApiConfig.api_key = api_key
    code = '3990'
    # result = quandl.get('TSE/' + code, returns="numpy")
    # print(result)
    # 取得できる件数に限りがあるようす(13営業日分?)
    """
    [(datetime.datetime(2017, 8, 30, 0, 0), nan, nan, nan, nan, 0.0)
    (datetime.datetime(2017, 8, 31, 0, 0), 6700.0, 6800.0, 6020.0, 6160.0, 1522600.0)
    (datetime.datetime(2017, 9, 1, 0, 0), 6360.0, 6420.0, 5460.0, 5540.0, 1372700.0)
    (datetime.datetime(2017, 9, 4, 0, 0), 5240.0, 5500.0, 4815.0, 5040.0, 1007200.0)
    (datetime.datetime(2017, 9, 5, 0, 0), 5200.0, 5360.0, 4730.0, 5190.0, 1362700.0)
    (datetime.datetime(2017, 9, 6, 0, 0), 5040.0, 5450.0, 4935.0, 4955.0, 1078600.0)
    (datetime.datetime(2017, 9, 7, 0, 0), 5020.0, 5120.0, 4650.0, 4670.0, 584700.0)
    (datetime.datetime(2017, 9, 8, 0, 0), 4715.0, 4765.0, 4400.0, 4500.0, 515600.0)
    (datetime.datetime(2017, 9, 11, 0, 0), 4570.0, 4860.0, 4435.0, 4850.0, 548400.0)
    (datetime.datetime(2017, 9, 12, 0, 0), 4895.0, 5070.0, 4640.0, 4680.0, 592000.0)
    (datetime.datetime(2017, 9, 13, 0, 0), 4675.0, 4835.0, 4650.0, 4750.0, 292100.0)
    (datetime.datetime(2017, 9, 14, 0, 0), 4715.0, 4755.0, 4500.0, 4570.0, 327400.0)
    (datetime.datetime(2017, 9, 15, 0, 0), 4500.0, 4650.0, 4460.0, 4615.0, 158000.0)]
    """

    # result = quandl.get('TSE/' + code, start_date='2017-08-29', end_date='2017-08-29', returns="numpy")
    # print(result)
    # 13営業日以前のデータは取得できなかった。
    """
    []
    """
    # →と思ったら、3990(Ummm)の上場が8/30でデータがないだけだった。他銘柄だと過去数年分取得できた。

    # result = quandl.get(["TSE/3990", "TSE/6045"], start_date='2017-09-11', end_date='2017-09-11', returns="numpy")
    # print(result)
    # 複数銘柄の取得だと、結果が一行に繋がるから、整形がかなりしんどい。
    """
    [ (datetime.datetime(2017, 9, 11, 0, 0), 4570.0, 4860.0, 4435.0, 4850.0, 548400.0, 888.0, 898.0, 882.0, 892.0, 46000.0)]
    """

    # result = quandl.get('TSE/' + code, start_date='2017-09-05', returns="numpy")
    # print(result)
    # 開始日のみの指定でも、取得可能。
    """
    [ (datetime.datetime(2017, 9, 5, 0, 0), 5200.0, 5360.0, 4730.0, 5190.0, 1362700.0)
    (datetime.datetime(2017, 9, 6, 0, 0), 5040.0, 5450.0, 4935.0, 4955.0, 1078600.0)
    (datetime.datetime(2017, 9, 7, 0, 0), 5020.0, 5120.0, 4650.0, 4670.0, 584700.0)
    (datetime.datetime(2017, 9, 8, 0, 0), 4715.0, 4765.0, 4400.0, 4500.0, 515600.0)
    (datetime.datetime(2017, 9, 11, 0, 0), 4570.0, 4860.0, 4435.0, 4850.0, 548400.0)
    (datetime.datetime(2017, 9, 12, 0, 0), 4895.0, 5070.0, 4640.0, 4680.0, 592000.0)
    (datetime.datetime(2017, 9, 13, 0, 0), 4675.0, 4835.0, 4650.0, 4750.0, 292100.0)
    (datetime.datetime(2017, 9, 14, 0, 0), 4715.0, 4755.0, 4500.0, 4570.0, 327400.0)
    (datetime.datetime(2017, 9, 15, 0, 0), 4500.0, 4650.0, 4460.0, 4615.0, 158000.0)]
    """

    result = quandl.get('TSE/' + code, start_date='2000-00-00', returns="numpy")
    print(result)
    """
    quandl.errors.quandl_error.InvalidRequestError: (Status 422) (Quandl Error QESx04) You have submitted incorrect query parameters. Please check your API call syntax and try again.
    """


def get_tables_data_test():
    conf = configparser.ConfigParser()
    conf.read('config.ini')
    api_key = conf.get('quandl', 'api_key')

    quandl.ApiConfig.api_key = api_key
    data = quandl.get_table('MER/F1', compnumber=39102, paginate=True)
    pprint(data)


if __name__ == "__main__":
    get_daily_data_test()