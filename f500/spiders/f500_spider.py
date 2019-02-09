from scrapy import Spider
from scrapy import Request
from f500.items import F500MasterItem, F500DetailItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.loader.processors import TakeFirst
import re


class F500Spider(Spider):
    name = 'f500_spider'
    allowed_urls = ['https://money.cnn.com/magazines/fortune/']
    masterLinksList = None

    start_year1 = 1955
    end_year1 = 1961

    start_year2 = 2006
    end_year2 = 2007


    xpath_sets = {
        'pre2008' : {
            'rows'      : '//table[@class="maglisttable"]//tr[@id="tablerow"]',
            'company'   : './/td[@class="company"]/a/text()',
            'rank'      : './/td[@class="rank"]/text()',
            'revenue'   : './/td[@class="revenue"]/text()',
            'datacells' : './/td[@class="datacell"]/text()',
            'detail_url': './/td[@class="company"]/a/@href'
        },
        'post2008': {
            'rows'      : '//div[@id="cnnmagFeatData"]//tbody//tr',
            'company'   : './td[@class="cnncol2"]/a/text()',
            'rank'      : './td[@class="cnncol1"]/text()',
            'revenue'   : './td[@class="cnncol3"]/text()',
            'datacells' : './td[@class="cnncol4"]/text()',
            'detail_url': './td[@class="cnncol2"]/a/@href'
        },
        'just2008': {
            'rows': '//table[@class="with220inset"]//tr[@id="tablerow"]',
            'company': './td[@class="alignLft"]/a/text()',
            'rank': './td[@class="alignRgt"]/text()',
            'revenue': './td[@class="alignRgt shadeCell"]/text()',
            'datacells': './td[@class="alignRgtB shadeCell"]/text()',
            'detail_url': './td[@class="alignLft"]/a/@href'
        }

    }

    def getMasterLinks(self):
        if self.masterLinksList == None:
            links = {}
            first = "https://money.cnn.com/magazines/fortune/fortune500_archive/full/"
            first_tail_ends = ["/1.html", "/101.html", "/201.html", "/301.html", "/401.html"]

            second = "https://money.cnn.com/magazines/fortune/fortune500/"
            second_tail_ends = ["/index.html", "/101_200.html", "/201_300.html", "/301_400.html", "/401_500.html"]

            for i in range(self.start_year1, self.end_year1):
                for j in first_tail_ends:
                    link = first + str(i) + j
                    links[link] = i

            for i in range(self.start_year2, self.end_year2):
                for j in second_tail_ends:
                    link = second + str(i) + "/full_list" + j
                    links[link] = i
            # links['file:///private/var/folders/b_/g8nmb1zd1zj0v01fb93_l8s00000gr/T/tmpsfpu1sn1.html'] = 2012
            # links['file:///private/var/folders/b_/g8nmb1zd1zj0v01fb93_l8s00000gr/T/tmpf58el64p.html'] = 2008

            self.masterLinksList = links
            print(self.masterLinksList )

        return self.masterLinksList

    def start_requests(self):

        urls = self.getMasterLinks().keys()

        print(urls)

        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):

        print("response URL : " + response.url)
        year_parsed = self.getMasterLinks().get(response.url)
        print("Year :" + str(year_parsed))

        if (year_parsed<2008):
            xpath_tags = self.xpath_sets.get("pre2008")
        elif (year_parsed > 2008):
            xpath_tags = self.xpath_sets.get("post2008")
        else:
            xpath_tags = self.xpath_sets.get("just2008")

        rows = response.xpath(xpath_tags.get('rows'))

        for row in rows:

            item_loader = ItemLoader(item=F500MasterItem(), selector=row)

            item_loader.default_output_processor = TakeFirst()

            item_loader.add_value('year', year_parsed)

            item_loader.add_xpath('company', xpath_tags.get('company') )
            item_loader.add_xpath('rank', xpath_tags.get('rank') )

            revenue = row.xpath(xpath_tags.get('revenue')).get()
            datacells = row.xpath(xpath_tags.get('datacells')).getall()

            if(revenue):
                item_loader.add_value('revenue', revenue )
                item_loader.add_value('profits', datacells)
            elif(datacells):
                if(len(datacells) == 2):
                    item_loader.add_value('revenue', datacells[0])
                    item_loader.add_value('profits', datacells[1])

            item_loader.add_xpath('detail_url', xpath_tags.get('detail_url') )
            item_loader.add_value('self_url', response.url )


            yield item_loader.load_item()

