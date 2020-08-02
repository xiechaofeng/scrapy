# -*- coding: utf-8 -*-
import scrapy
import re

from lianjia.items import LianjiaItem
class LianjiaspiderSpider(scrapy.Spider):
    name = 'lianjiaspider'
    allowed_domains = ['sh.lianjia.com']
    baseURL = 'https://sh.lianjia.com'
    start_urls = [baseURL+'/ditiefang/pg1']


    def parse(self, response):
        regionURL = response.xpath("//div[@data-role='ditiefang']/div/a/@href").extract()
        for url in regionURL:
            yield scrapy.Request(self.baseURL + url, callback=self.detailparse)

    def detailparse(self, response):
        node_list = response.xpath("//div[@class='info clear']")
        regionURL = response.xpath("//div[@data-role='ditiefang']/div[1]/a/@href").extract()
        region = response.xpath("//div[@data-role='ditiefang']/div[1]/a/text()").extract()
        select = response.xpath("//div[@data-role='ditiefang']/div[1]/a[@class='selected']/text()").extract()[0]
        urlseg = regionURL[region.index(select)]
        page_data = eval(response.xpath("//div/@page-data").extract()[0])
        for node in node_list:
            item = LianjiaItem()
            item['region'] = select
            item['title'] = node.xpath("./div[@class='title']/a/text()").extract()[0].replace(',','，')
            item['titleLink'] = node.xpath("./div[@class='title']/a/@href").extract()[0]
            item['houseType'] = node.xpath("./div[@class='title']/a/@data-el").extract()[0]
            item['totalPrice'] = node.xpath("./div[@class='priceInfo']/div[@class='totalPrice']/span/text() ").extract()[0]
            item['unit'] = node.xpath("./div[@class='priceInfo']/div[@class='totalPrice']/text() ").extract()[0]
            item['unitPrice'] = re.search('[\d\.]+',node.xpath("./div[@class='priceInfo']/div[@class='unitPrice']/span/text()").extract()[0]).group()
            item['houseInfo'] = node.xpath("./div[@class='address']/div[@class='houseInfo']/text()").extract()[0]
            houseinfo = node.xpath("./div[@class='address']/div[@class='houseInfo']/text()").extract()[0].strip(' ').strip('|').split('|')
            item['roomType'] = houseinfo[0]
            item['area'] = re.search('[\d\.]+',houseinfo[1]).group()
            item['orientation'] = houseinfo[2]
            item['decoration'] = houseinfo[3]
            item['community'] = node.xpath("./div[@class='address']/div[@class='houseInfo']/a/text()").extract()[0]
            item['communityLink'] = node.xpath("./div[@class='address']/div[@class='houseInfo']/a/@href").extract()[0]
            num = re.findall('\d+',node.xpath("./div[@class='flood']/div[@class='positionInfo']/text()").extract()[0])
            if len(num) > 1:
                item['floor'] = num[0]
                item['buildYear'] = num[1]
            else:
                item['floor'] = num[0]
                item['buildYear'] = ''
            item['location'] = node.xpath("./div[@class='flood']/div[@class='positionInfo']/a/text()").extract()[0]
            item['locationLink'] = node.xpath("./div[@class='flood']/div[@class='positionInfo']/a/@href").extract()[0]
            info = node.xpath("./div[@class='followInfo']/text()").extract()[0].split('/')
            item['followInfo'] = re.findall('\d+',info[0])[0]
            item['publishTime'] = info[1]
            yield item

        if page_data['curPage'] < page_data['totalPage']:
            offset = page_data['curPage'] + 1
            url = '/'.join([self.baseURL, '/'.join(urlseg.strip('/').split('/')[:-1]), 'pg'+str(offset)])
            print(url)
            yield scrapy.Request(url, callback=self.detailparse)