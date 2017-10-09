# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import MySQLdb


class ValidationPipeline(object):
    """
    Itemを検証するPipeline.
    """

    def process_item(self, item, spider):
        if not item['code']:
            # codeフィールドが取得出来ていない場合は破棄する.
            # DropItem()の引数は破棄する理由を表すメッセージ.
            raise DropItem('Missing code')

        return item  # codeフィールドが正しく取得できている場合.


class MySQLPipeline(object):
    """
    ItemをMySQLに保存するPipeline.
    """

    def open_spider(self, spider):
        """
        Spiderの開始時にMySQLに接続する.
        itemsテーブルがない場合は作成する.
        """

        settings = spider.settings  # settings.pyから設定を読み込む.
        params = {
            'host': settings.get('MYSQL_HOST', 'localhost'),  # ホスト
            'db': settings.get('MYSQL_DATABASE', 'stock_ver2'),  # データベース名
            'user': settings.get('MYSQL_USER', 'root'),  # ユーザー名
            'passwd': settings.get('MYSQL_PASSWORD', ''),  # パスワード
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),  # 文字コード
        }
        self.conn = MySQLdb.connect(**params)  # MySQLサーバーに接続.
        self.c = self.conn.cursor()  # カーソルを取得.
        # stock_app_fundamentals_dataテーブルが存在しない場合は作成.
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS stock_app_fundamentals_data (
                code int(11) NOT NULL,
                name CHAR(200) NOT NULL,
                market_capitalization int(11) NOT NULL,
                outstanding_shares int(11) NOT NULL,
                PRIMARY KEY (code)
            )
        ''')
        self.conn.commit()  # 変更をコミット.

    def close_spider(self, spider):
        """
        Spiderの終了時にMySQLサーバーへの接続を切断する.
        """

        self.conn.close()

    def process_item(self, item, spider):
        """
        Itemをstock_app_fundamentals_dataテーブルに挿入する.
        """

        # パラメーターが辞書の場合、プレースホルダーは %(名前)s で指定する.
        update_query = '''
            UPDATE stock_app_fundamentals_data set
                name = %(name)s, market_capitalization = %(market_capitalization)s, outstanding_shares = %(outstanding_shares)s
            WHERE code = %(code)s
                       '''

        insert_query = '''
            INSERT INTO stock_app_fundamentals_data 
                VALUES (%(code)s, %(name)s, %(market_capitalization)s, %(outstanding_shares)s)
                       '''

        # insert or update
        result = self.c.execute(update_query, dict(item))
        if result == 0:  # 0 = false
            self.c.execute(insert_query, dict(item))

        self.conn.commit()  # 変更をコミット.
        return item