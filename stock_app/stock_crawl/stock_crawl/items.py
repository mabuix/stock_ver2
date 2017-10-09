# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Fundamentals(scrapy.Item):
    """
    ファンダメンタル情報を表すItem.
    """

    # 銘柄コード
    code = scrapy.Field()
    # 銘柄名
    name = scrapy.Field()
    # 時価総額
    market_capitalization = scrapy.Field()
    # 発行済株式数
    outstanding_shares = scrapy.Field()