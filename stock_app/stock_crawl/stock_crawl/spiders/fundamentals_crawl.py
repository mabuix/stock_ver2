from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import os

# ItemのFundamentalsクラスをインポート.
from stock_crawl.items import Fundamentals


class FundamentalsCrawlSpider(CrawlSpider):
    # Spiderの名前.
    name = 'fundamentals_crawl'
    # クロール対象とするドメインのリスト.
    allowed_domains = ['stocks.finance.yahoo.co.jp']

    code_file_path = '../../code.txt'
    # ファイルの存在チェック.
    is_file_exist = os.path.exists(code_file_path)
    if not is_file_exist:
        raise FileNotFoundError('証券コードの読み込みファイルがありません。')

    url = 'https://stocks.finance.yahoo.co.jp/stocks/detail/?code='
    # クロールを開始するURLのリスト.
    start_urls = []
    # スクレイピング対象銘柄コードをファイルから読み込んで、銘柄紹介ページURLのリストを作る.
    with open(code_file_path, 'r') as codes:
        for code in codes:
            start_urls.append(url + code.rstrip())


    def parse(self, response):
        """
        銘柄詳細のページからファンダメンタル情報を抜き出す.
        """

        # Fundamentalsオブジェクトを作成.
        item = Fundamentals()
        code = response.css('#stockinf > div.stocksDtl.clearFix > div.forAddPortfolio > dl > dt::text').extract_first()
        item['code'] = int(code)
        # 先頭から、「【」まで抽出
        item['name'] = response.css('title::text').re_first('^[^【]*')
        market_capitalization = response.css('#rfindex > div.chartFinance > div:nth-child(1) > dl > dd > strong::text').extract_first()
        item['market_capitalization'] = int(market_capitalization.replace(',', ''))
        outstanding_shares = response.css('#rfindex > div.chartFinance > div:nth-child(2) > dl > dd > strong::text').extract_first()
        item['outstanding_shares'] = int(outstanding_shares.replace(',', ''))
        yield item  # Itemをyieldして、データを抽出する.