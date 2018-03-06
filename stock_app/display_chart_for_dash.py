import dash
from dash.dependencies import Input, Output, Event, State
import dash_core_components as dcc
import dash_html_components as html
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
import colorlover as cl
import numpy as np
import pandas as pd


"""
dash + SQLAlchemyを使用したチャート表示用のwebアプリケーション。
python実行でアプリケーションサーバー起動。
"""

"""
DBからデータ取得
"""
Base = declarative_base()


class Fundamental(Base):
    __tablename__ = 'stock_app_fundamentals_data'

    code = Column(Integer, primary_key=True)
    name = Column(String)
    market_capitalization = Column(Integer)
    outstanding_shares = Column(Integer)

    def __repr__(self):
        return "<Fundamental(code='%s',name='%s',market_capitalization='%s',outstanding_shares='%s')>"%(
            self.code, self.name, self.market_capitalization, self.outstanding_shares
        )


class Daily(Base):
    __tablename__ = 'stock_app_dailydata'

    id = Column(Integer, primary_key=True)
    code = Column(Integer)
    date = Column(Date)
    open = Column(Integer)
    high = Column(Integer)
    low = Column(Integer)
    close = Column(Integer)
    volume = Column(Integer)

    def __repr__(self):
        return "<Fundamental(id='%s',code='%s',date='%s',open='%s',high='%s',low='%s',close='%s',volume='%s')>" % (
            self.id, self.code, self.date, self.open, self.high, self.low, self.close, self.volume
        )


# ローカルのmysql stock_ver2データベースに接続.
# echo=Trueでロギング設定.
conn = sa.create_engine("mysql://root:@localhost/stock_ver2", echo=True)
Session = sessionmaker(bind=conn)
session = Session()


"""
dashを使ってチャートをブラウザ表示
"""
colorscale = cl.scales['9']['qual']['Paired']  # https://plot.ly/ipython-notebooks/color-scales/
# チャートの開始日
start_date = '2017-01-01'
# todo code.txtの読み込み
codes = [6094, 3550]
app = dash.Dash()
app.layout = html.Div([
    html.Div([
        html.H2('監視銘柄チャート'),
    ]),

    dcc.Input(id='my-id', value=codes, type="hidden"),
    html.Div(id='graphs')
])


@app.callback(
    Output('graphs', 'children'),
    [Input(component_id='my-id', component_property='value')]
)
def graphs(input_value):
    graphs = []
    codes = input_value
    query = session.query(Fundamental).filter(Fundamental.code.in_(codes))
    for fundamental in query.all():
        code = fundamental.code
        query = "select * from stock_app_dailydata where code = " + str(code) \
                + " and date >= " + str(start_date) + " order by date"
        df = pd.read_sql_query(query, conn)
        df['date'] = pd.to_datetime(df['date'])
        df['weekday'] = df['date'].dt.dayofweek
        df['day_of_week'] = df['date'].dt.weekday_name

        candlestick = {
            # 'x': date_list,
            'open': df['open'],
            'high': df['high'],
            'low': df['low'],
            'close': df['close'],
            'type': 'candlestick',
            'name': code,
            'legendgroup': code,
            'yaxis': 'y4',
            'increasing': {'name': 'incr', 'line': {'color': colorscale[0]}},
            'decreasing': {'name': 'decr', 'line': {'color': colorscale[1]}}
        }

        ma8 = {
            # 'x': date_list,
            'y': moving_average(df['close'], 8),
            'type': 'scatter', 'mode': 'lines',
            'line': {'width': 1, 'color': colorscale[2]},
            'legendgroup': code,
            'yaxis': 'y4',
            'name': '8MA'
        }

        ma13 = {
            # 'x': date_list,
            'y': moving_average(df['close'], 13),
            'type': 'scatter', 'mode': 'lines',
            'line': {'width': 1, 'color': colorscale[3]},
            'legendgroup': code,
            'yaxis': 'y4',
            'name': '13MA'
        }

        ma21 = {
            # 'x': date_list,
            'y': moving_average(df['close'], 21),
            'type': 'scatter', 'mode': 'lines',
            'line': {'width': 1, 'color': colorscale[4]},
            'legendgroup': code,
            'yaxis': 'y4',
            'name': '21MA'
        }

        volume_bar = {
            # 'x': date_list,
            'y': df['volume'],
            'type': 'bar',
            'yaxis': 'y3',
            'name': 'Volume'
        }

        d = {
            # 'x': date_list,
            'y': stochastic_D(df['close'], df['high'], df['low'], period_K=5, period=3),
            'type': 'scatter', 'mode': 'lines',
            'yaxis': 'y2',
            'name': '%D'
        }

        sd = {
            # 'x': date_list,
            'y': stochastic_slowD(df['close'], df['high'], df['low'], period_K=5, period_D=5, period=3),
            'type': 'scatter', 'mode': 'lines',
            'yaxis': 'y2',
            'name': 'SD'
        }

        macd = {
            # 'x': date_list,
            'y': MACD(df['close'], short_period=12, long_period=26),
            'type': 'scatter', 'mode': 'lines',
            'yaxis': 'y',
            'name': 'MACD'
        }

        macd_signal = {
            # 'x': date_list,
            'y': MACD_signal(df['close'], short_period=12, long_period=26, signal_period=9),
            'type': 'scatter', 'mode': 'lines',
            'yaxis': 'y',
            'name': 'MACD_signal'
        }

        graphs.append(dcc.Graph(
            id='code_' + str(code),
            figure={
                'data': [candlestick] + [ma8] + [ma13] + [ma21] + [volume_bar] + [d] + [sd] + [macd] + [macd_signal],
                'layout': {  # ドキュメント: https://plot.ly/python/reference/#layout
                    'title': str(code) + ' - ' + fundamental.name,

                    # グラフの画面サイズ調整
                    'height': 700,
                    'margin': {'b': 0, 'r': 10, 'l': 60, 't': 40},

                    # 見出しの調整
                    # 'legend': {'x': 0},
                    # 'legend': {'orientation': 'h', 'y': 0.9, 'x': 0.3, 'yanchor': 'bottom'},
                    'legend': {'orientation': 'h', 'y': 1, 'x': 0},

                    'xaxis': {'showgrid': True,  # 縦グリッドラインの表示
                              # ティックごとの位置に表示されるテキストの指定(日時を表示)
                              'ticktext': [x for x in df['date']],
                              # 表示するティックを指定(全表示)
                              'tickvals': [x for x in df.index],

                              # rangeslider(画面下のグラフ)の非表示
                              'rangeslider': {'visible': False, 'thickness': 0.15},

                              # rangeselector(グラフ右上の期間選択ボタン)の表示
                              'rangeselector': {'visible': True,
                                                'buttons': [
                                                    {'count': 1, 'label': '1m', 'step': 'month', 'stepmode': 'backward'},
                                                    {'count': 6, 'label': '6m', 'step': 'month', 'stepmode': 'backward'},
                                                    {'count': 1, 'label': 'YTD', 'step': 'year', 'stepmode': 'todate'},
                                                    {'count': 1, 'label': '1y', 'step': 'year', 'stepmode': 'backward'},
                                                    {'step': 'all'}
                                                ]}},

                    # 表示するグラフごとにy座標の範囲を指定
                    'yaxis': {'domain': [0, 0.166], 'showticklabels': False},
                    'yaxis2': {'domain': [0.17, 0.336], 'showticklabels': False},
                    'yaxis3': {'domain': [0.34, 0.506], 'showticklabels': False},
                    'yaxis4': {'domain': [0.506, 1]},
                }
            },
        ))

    return graphs


def moving_average(interval, window_size=10):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')


def stochastic_K(end, high, low, period):
    """
    ストキャスティクス の %K を計算
    """

    hline = high.rolling(period).max()
    lline = low.rolling(period).min()
    return (end - lline) / (hline - lline)


def stochastic_D(end, high, low, period_K, period):
    """
    ストキャスティクス の %D を計算
    """

    hline = high.rolling(period_K).max()
    lline = low.rolling(period_K).min()

    sumlow = (end - lline).rolling(period).sum()
    sumhigh = (hline - lline).rolling(period).sum()

    return sumlow / sumhigh


def stochastic_slowD(end, high, low, period_K, period_D, period):
    """
    ストキャスティクス の SlowD を計算
    """
    d = stochastic_D(end, high, low, period_K, period_D)
    return d.rolling(period).mean()


def MACD(close, short_period, long_period):
    """
    MACD とその signal を計算
    """

    shorts = close.ewm(span=short_period).mean()
    longs = close.ewm(span=long_period).mean()
    _macd = shorts - longs
    return _macd


def MACD_signal(close, short_period, long_period, signal_period):
    macd = MACD(close, short_period, long_period)
    return macd.ewm(span=signal_period).mean()


# todo ページングをつける

if __name__ == '__main__':
    app.run_server(debug=True)
