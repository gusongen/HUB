# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BbbItem(scrapy.Item):
#定义item的属性
     name = scrapy.Field()
     link = scrapy.Field()
     date = scrapy.Field() 
     quyu=scrapy.Field() 
     zhonbiaodanwei=scrapy.Field() 
     details = scrapy.Field() 
     