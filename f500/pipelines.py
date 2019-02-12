# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter



class WriteItemPipeline(object):

    def open_spider(self, spider):
        self.year_to_exporter = {}

    def close_spider(self, spider):
        """
        Close all open exporters
        :param spider: Current instance of spider
        :return: None
        """
        for exporter in self.year_to_exporter.values():
            exporter.finish_exporting()
            exporter.stream.close()

    def process_item(self, item, spider):
        # self.exporter.export_item(item)
        # return item
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)

        return item

    def _exporter_for_item(self, item):
        """
        Create an exporter per year, store in master list and return the exporter
        :param item: Scrapped Item
        :return: CvsItemExporter
        """
        year = item['year']
        if year not in self.year_to_exporter:
            file = open('data/{}_master.csv'.format(year), 'wb')
            exporter = CsvItemExporter(file)
            exporter.start_exporting()
            self.year_to_exporter[year] = exporter
        return self.year_to_exporter[year]
