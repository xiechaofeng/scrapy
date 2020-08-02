# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    region = scrapy.Field()
    title = scrapy.Field()
    titleLink = scrapy.Field()
    houseType = scrapy.Field()
    totalPrice = scrapy.Field()
    unit = scrapy.Field()
    unitPrice = scrapy.Field()
    houseInfo = scrapy.Field()
    roomType = scrapy.Field()
    area = scrapy.Field()
    orientation = scrapy.Field()
    decoration = scrapy.Field()
    community = scrapy.Field()
    communityLink = scrapy.Field()
    floor = scrapy.Field()
    buildYear = scrapy.Field()
    location = scrapy.Field()
    locationLink = scrapy.Field()
    followInfo = scrapy.Field()
    publishTime = scrapy.Field()
