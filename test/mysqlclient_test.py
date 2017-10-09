import MySQLdb

params = {
    'host': 'localhost',  # ホスト
    'db': 'stock_ver2',  # データベース名
    'user': 'root',  # ユーザー名
    'passwd': '',  # パスワード
    'charset': 'utf8mb4',  # 文字コード
}
conn = MySQLdb.connect(**params)  # MySQLサーバーに接続.
c = conn.cursor()  # カーソルを取得.

insert_query = '''
    INSERT INTO stock_app_fundamentals_data 
        (code, name, market_capitalization, outstanding_shares)
        VALUES (9999, 'テスト', 9999999, 9999999)
               '''

update_query = '''
    UPDATE stock_app_fundamentals_data set
        name = 'テスト', market_capitalization = 1111111, outstanding_shares = 1111111
    WHERE code = 9999
               '''

delete_query = '''
    DELETE FROM stock_app_fundamentals_data
    WHERE code = 9999
               '''

result = c.execute(update_query)
# 0 (false)
print(result)

result = c.execute(delete_query)
# 0 (false)
print(result)

result = c.execute(insert_query)
# 1 (true)
print(result)

result = c.execute(update_query)
# 1 (true)
print(result)

result = c.execute(delete_query)
# 1 (true)
print(result)

conn.commit()  # 変更をコミット.