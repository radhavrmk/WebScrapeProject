# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter

#
# class F500Pipeline(object):
#     def process_item(self, item, spider):
#         print("in wrong process")
#         return item

# class URLPipeline(object):
#     def __init__(self):
#         self.filename = '/URL/detail_URL.csv'
#     def open_spider(self, spider):
#         self.csvfile = open(self.filename, 'ab')
#         self.exporter = CsvItemExporter(self.csvfile)
#         self.exporter.start_exporting()
#     def close_spider(self, spider):
#         self.exporter.finish_exporting()
#         self.csvfile.close()
#     def process_item(self, item, spider):
#         print("in Exporter process")
#         self.exporter.export_item(item)
#         return item


class WriteItemPipeline(object):
    # def __init__(self):
        # self.filename = 'data/F500_master.csv'
        # self.year_to_exporter = {}

    def open_spider(self, spider):
        # # self.csvfile = open(self.filename, 'wb')
        # # self.exporter = CsvItemExporter(self.csvfile)
        # self.exporter.start_exporting()
        self.year_to_exporter = {}

    def close_spider(self, spider):
        # self.exporter.finish_exporting()
        # self.csvfile.close()
        for exporter in self.year_to_exporter.values():
            exporter.finish_exporting()
            print(str(exporter))
            print(str(exporter.csv_writer))
            exporter.stream.close()
            # exporter.file.close()

    def process_item(self, item, spider):
        # self.exporter.export_item(item)
        # return item
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)

        return item

    def _exporter_for_item(self, item):
        year = item['year']
        if year not in self.year_to_exporter:
            file = open('data/{}_master.csv'.format(year), 'wb')
            exporter = CsvItemExporter(file)
            exporter.start_exporting()
            self.year_to_exporter[year] = exporter
        return self.year_to_exporter[year]
