# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JingdongItem(scrapy.Item):
	price=scrapy.Field()
	title=scrapy.Field()
	link=scrapy.Field()
	pic_url=scrapy.Field()
	number=scrapy.Field()
	#comment=scrapy.Field()
	    
	   
