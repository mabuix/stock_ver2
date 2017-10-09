from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import os

# ItemのFundamentalsクラスをインポート.
from stock_crawl.items import Fundamentals

"""
ファンダメンタル情報を全銘柄取得(※サイトに負荷かけるので実行注意)
"""

class FundamentalsCrawlAllSpider(CrawlSpider):
    # Spiderの名前.
    name = 'fundamentals_crawl_all'
    # クロール対象とするドメインのリスト.
    allowed_domains = ['stocks.finance.yahoo.co.jp']
    # クロールを開始するURLのリスト.
    start_urls = ['https://stocks.finance.yahoo.co.jp/stocks/qi/?js=あ']

    # リンクをたどるためのルールのリスト.
    rules = (
        # 五十音銘柄一覧 → 銘柄詳細のページへのリンクをたどり、レスポンスをparse_detail()メソッドで処理する.
        Rule(LinkExtractor(allow=r'/stocks/qi/\?js=.+')),
        Rule(LinkExtractor(allow=r'/stocks/detail/\?code=\w+'), callback='parse_detail'),
    )


    def parse_detail(self, response):
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