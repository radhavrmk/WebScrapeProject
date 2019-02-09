# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose
import re

# def parse_year(year_str):
#     if year_str:
#         return re.findall("\d+",year_str)

def parse_int(int_str):
    if int_str:
        try:
            return int(int_str)
        except:
            return None

def trim_str(str_to_trim):
    if str_to_trim:
        return re.sub("\s+"," ", str_to_trim)

def parse_dollar(dollar_str):
    if dollar_str:
        print("Dollar Str")
        print(dollar_str)
        try:
            converted = float(re.sub("[+s,]+","",dollar_str))
            return converted
        except:
            return None

def adjust_detailURL(url):
    if(url):
        return re.sub("(\.\./\.\.)+", "https://money.cnn.com/magazines/fortune/fortune500_archive",url)

class F500DetailItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    year = scrapy.Field()
    rank = scrapy.Field()
    company = scrapy.Field()
    URL = scrapy.Field()

    revenue = scrapy.Field()
    revenue_rank = scrapy.Field()

    profits = scrapy.Field()
    profits_rank = scrapy.Field()

    assets = scrapy.Field()
    assets_rank = scrapy.Field()

    stk_equity = scrapy.Field()
    stk_equity_rank = scrapy.Field()

    market_cap = scrapy.Field()
    market_cap_rank = scrapy.Field()

    employee_count = scrapy.Field()
    employee_count_rank = scrapy.Field()

    EPS = scrapy.Field()
    EPS_10yr_growth = scrapy.Field()
    total_return_10yr = scrapy.Field()
    total_return_10yr_rank = scrapy.Field()


class F500MasterItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    year = scrapy.Field(
        # input_processor = MapCompose(parse_year)
    )
    company = scrapy.Field(
        input_processor=MapCompose(trim_str)
    )
    rank = scrapy.Field(
        input_processor=MapCompose(parse_int)
    )
    revenue = scrapy.Field(
        input_processor=MapCompose(parse_dollar)
    )
    profits = scrapy.Field(
        input_processor=MapCompose(parse_dollar)
    )
    self_url = scrapy.Field()
    detail_url = scrapy.Field(
        input_processor=MapCompose(adjust_detailURL)
    )
