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
            'rows': '//div[@id="cnnmagFeatData"]//tbody//tr',
            'company': './td[@class="cnncol2"]/a/text()',
            'rank': './td[@class="cnncol1"]/text()',
            'revenue': './td[@class="cnncol3"]/text()',
            'datacells': './td[@class="cnncol4"]/text()',
            'detail_url': './td[@class="cnncol2"]/a/@href'
        }

    }

    def masterLinkGenerator():

        links = []
        first = "https://money.cnn.com/magazines/fortune/fortune500_archive/full/"
        first_tail_ends = ["/1.html", "/101.html", "/201.html", "/301.html", "/401.html"]

        second = "https://money.cnn.com/magazines/fortune/fortune500/"
        second_tail_ends = ["/index.html", "/101_200.html", "/201_300.html", "/301_400.html", "/401_500.html"]

        for i in range(1955, 2006):
            for j in first_tail_ends:
                link = first + str(i) + j
                links.append(link)

        for i in range(2006, 2013):
            for j in second_tail_ends:
                link = second + str(i) + "/full_list" + j
                links.append(link)

        return links

    def start_requests(self):
        urls = [
            # 'file:///private/var/folders/b_/g8nmb1zd1zj0v01fb93_l8s00000gr/T/tmpg09k08yh.html',
            # 'file:///private/var/folders/b_/g8nmb1zd1zj0v01fb93_l8s00000gr/T/tmpdj2id8ug.html',
            # 'file:///private/var/folders/b_/g8nmb1zd1zj0v01fb93_l8s00000gr/T/tmpzdzvzwk5.html'
            # 'file:///private/var/folders/b_/g8nmb1zd1zj0v01fb93_l8s00000gr/T/tmpr_xkurs8.html'
            'file:///private/var/folders/b_/g8nmb1zd1zj0v01fb93_l8s00000gr/T/tmpafmlr6j8.html'
        ]

        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):

        year = response.xpath('//div[@id="MagListDataTable"]//td[@class="titlerow"]/text()').get()
        print(1)
        if (year):
            year_parsed = int(re.findall("\d+",year)[0])
        else:
            year_parsed = 2012
        print(2)

        if (year_parsed<2008):
            xpath_tags = self.xpath_sets.get("pre2008")
        elif (year_parsed > 2008):
            xpath_tags = self.xpath_sets.get("post2008")
        else:
            xpath_tags = self.xpath_sets.get("just2008")
        print(3)

        rows = response.xpath(xpath_tags.get('rows'))

        for row in rows:
            # item = F500MasterItem()
            # item["detail_url"] = row.xpath('.//td[@class="company"]/a/@href').get()
            # item["company"] = row.xpath('.//td[@class="company"]/a/text()').get()
            # item["rank"] = row.xpath('.//td[@class="rank"]/text()').get()
            # temp = row.xpath('.//td[@class="datacell"]/text()').getall()
            # temp2 = row.xpath('.//td[@class="radha"]/text()').get()
            # print(temp2)
            # if(temp != None):
            #     item["revenue"] = temp[0]
            #     item["profits"] = temp[1]
            # item["year"] = year
            # item["self_url"] = temp2
            # print(item)

            item_loader = ItemLoader(item=F500MasterItem(), selector=row)

            item_loader.default_output_processor = TakeFirst()

            item_loader.add_value('year', year_parsed)
            # item_loader.add_xpath('company', './/td[@class="company"]/a/text()' )
            # item_loader.add_xpath('rank', './/td[@class="rank"]/text()' )
            #
            # revenue = row.xpath('.//td[@class="revenue"]/text()').get()
            # datacells = row.xpath('.//td[@class="datacell"]/text()').getall()

            item_loader.add_xpath('company', xpath_tags.get('company') )
            item_loader.add_xpath('rank', xpath_tags.get('rank') )

            revenue = row.xpath(xpath_tags.get('revenue')).get()
            datacells = row.xpath(xpath_tags.get('datacells')).getall()



            if(revenue):
                item_loader.add_value('revenue', revenue )
            elif(datacells):
                # print(len(datacells))
                if(len(datacells) == 2):
                    item_loader.add_value('revenue', datacells[0])
                    item_loader.add_value('profits', datacells[1])

            item_loader.add_xpath('detail_url', xpath_tags.get('detail_url') )
            item_loader.add_value('self_url', response.url )


            yield item_loader.load_item()

