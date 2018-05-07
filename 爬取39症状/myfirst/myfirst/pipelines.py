# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

class MyfirstPipeline(object):
    def __init__(self):
        self.file = open('症状.txt', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        self.file.write(item['name'] + '  ' + item['url'] + '\n')
        return item

    def close_spider(self, spider):
        self.file.close()
