# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
class LianjiaPipeline(object):
    def __init__(self):
        self.f = open('lianjia_ditiefang.csv','w')
    def process_item(self, item, spider):
        houseItem = dict(item)
        content = ','.join(houseItem.values()) + '\n'
        self.f.write(content)
        return item
    def close_spider(self,spider):
        self.f.close()
