# -*- coding: utf-8 -*-
import scrapy
import os
from boohee.items import BooheeItem

class BooheespiderSpider(scrapy.Spider):
    name = 'booheespider'
    allowed_domains = ['boohee.com']
    start_urls = ['http://boohee.com/food/']
    baseURL = 'http://boohee.com/'

    def parse(self, response):
        foodURL = response.xpath("//h3/a/@href").extract()
        for url in foodURL:
            yield scrapy.Request(os.path.join(self.baseURL, url.strip('/')),
                                 meta={'dont_redirect': True, 'handle_httpstatus_list': [301]},
                                 callback=self.foodparse, dont_filter=True)

    def foodparse(self, response):
        limit_page = int(response.xpath("//div/@limit_page").extract()[0])
        page = response.xpath("//a[@class='next_page']/@href").extract()[0][:-1].strip('/')
        for i in range(1, limit_page+1):
            yield scrapy.Request(os.path.join(self.baseURL, page+str(i)),
                                 meta={'dont_redirect': True, 'handle_httpstatus_list': [301]},
                                 callback=self.detailparse, dont_filter=True)

    def detailparse(self, response):
        foodURLs = response.xpath("//div/h4/a/@href").extract()
        for url in foodURLs:
            yield scrapy.Request(os.path.join(self.baseURL, url.strip('/')),
                                 meta={'dont_redirect': True, 'handle_httpstatus_list': [301]},
                                 callback=self.infoparse, dont_filter=True)

    def infoparse(self, response):
        item = BooheeItem()
        item['name'] = response.xpath("//div/h2/text()[2]").extract()[0].strip().strip('/')
        item['imgurl'] = response.xpath("//div[@class='content']/div/div/a/@href").extract()[0]
        alia = response.xpath("//ul[@class='basic-infor']/li/text()").extract()
        if alia:
            item['alia'] = alia[0]
        else:
            item['alia'] = ''
        # category = response.xpath("//ul[@class='basic-infor']/li/strong/a/text()").extract()
        # if category:
        #     item['category'] = category[0]
        # else:
        #     item['category'] = ''
        item['category'] = response.xpath("//div[@class='clearfix']/ul/li/strong/a/text()").extract()[0]
        item['review'] = response.xpath("//div[@class='content']/p/text()").extract()[1].replace(',', '，').strip()
        item['calory'] = response.xpath("//dd/span/span/text()").extract()[0]
        nutrients = response.xpath("//dd/span[@class='dd']/text()").extract()[2:]
        if len(nutrients) == 22:
            item['carbohydrate'] = nutrients[0]
            item['fat'] = nutrients[1]
            item['protein'] = nutrients[2]
            item['fiber'] = nutrients[3]
            item['vitaminA'] = nutrients[4]
            item['vitaminC'] = nutrients[5]
            item['vitaminE'] = nutrients[6]
            item['carotene'] = nutrients[7]
            item['thiamine'] = nutrients[8]
            item['riboflavin'] = nutrients[9]
            item['niacin'] = nutrients[10]
            item['cholesterol'] = nutrients[11]
            item['Mg'] = nutrients[12]
            item['Ca'] = nutrients[13]
            item['Fe'] = nutrients[14]
            item['Zn'] = nutrients[15]
            item['Cu'] = nutrients[16]
            item['Mn'] = nutrients[17]
            item['K'] = nutrients[18]
            item['P'] = nutrients[19]
            item['Na'] = nutrients[20]
            item['Se'] = nutrients[21]
        else:
            item['carbohydrate'] = nutrients[0]
            item['fat'] = nutrients[1]
            item['protein'] = nutrients[2]
            item['fiber'] = nutrients[3]
        yield item


