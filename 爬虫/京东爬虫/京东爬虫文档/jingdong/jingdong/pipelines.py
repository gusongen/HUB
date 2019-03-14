# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from urllib import urlretrieve
class JingdongPipeline(object):
	def process_item(self, item, spider):
		#try:
        	r_url = item['pic_url']
        	print("--------------------------"+r_url)
        	file = '/home/lgw/'+item["number"]+'.jpg'
        	urlretrieve(r_url,file)
        	return item
		
	
