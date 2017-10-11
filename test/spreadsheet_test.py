import gspread
from oauth2client.service_account import ServiceAccountCredentials

"""
スプレッドシート操作用に作成したGoogle APIsプロジェクトのユーザーを、操作したいシートに権限追加して使用する。
ユーザー情報は、発行されたService Account Key内の、client_emailに記載。
% cat /Users/manatonakane/git/stock_ver2/sandbox-a739dfc2f0da.json
"""

scope = ['https://spreadsheets.google.com/feeds']

# 発行されたService Account Key(jsonファイル)を指定する
credentials = ServiceAccountCredentials.from_json_keyfile_name('../sandbox-a739dfc2f0da.json', scope)

gc = gspread.authorize(credentials)

# ユーザー追加したスプレッドシートの名前を指定する
# スプレッドシートの名称以外に、
# URLに含まれるIDで開くopen_by_key、URL自体を指定してスプレッドシートを開くopen_by_url
# というメソッドもある。　Credentialのメールアドレスでパーミッションが与えられているものしか開けない
# ので、注意！
# wks = gc.open("gspreadテスト").sheet1

# A1セルの値を取得
# print(wks.acell('A1'))

# A1セルを更新
# wks.update_acell('A1', u'Hello, gspread.')

# ワークブックを開く
workbook = gc.open("gspreadテスト")

# シート名を指定して開く
try:
    worksheet = workbook.worksheet("test")
    # 開けたら、内容リセットするためワークシートを削除
    workbook.del_worksheet(worksheet)
except gspread.exceptions.WorksheetNotFound:
    pass

# ワークシートを作成
worksheet = workbook.add_worksheet(title="test", rows="100", cols="20")

# update cell
worksheet.update_acell('A1', 'コード')
worksheet.update_acell('B1', '名称')
worksheet.update_acell('C1', '日時')
worksheet.update_acell('D1', '株価')
worksheet.update_acell('E1', '時価総額')
worksheet.update_acell('F1', '発行済株式数')

# Select a range
cell_list = worksheet.range('A2:F7')

for cell in cell_list:
    cell.value = 'O_o'

# Update in batch
worksheet.update_cells(cell_list)

