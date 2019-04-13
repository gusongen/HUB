# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

"""
class HhhPipeline(object):
    def process_item(self, item, spider):
        return item

import csv
import os
class Pipeline_ToCSV(object):
 
    def __init__(self):
        #csv文件的位置,无需事先创建
        store_file = os.path.dirname(__file__) + '/spiders/qtw.csv'
        #打开(创建)文件
        self.file = open(store_file,'wb')
        #csv写法
        self.writer = csv.writer(self.file)
        
    def process_item(self,item,spider):
        #判断字段值不为空再写入文件
        if item['image_name']:
            self.writer.writerow((item['image_name'].encode('utf8','ignore'),item['image_urls']))
        return item
    
    def close_spider(self,spider):
        #关闭爬虫时顺便将文件保存退出
        self.file.close()        
"""
from openpyxl import Workbook

class  HhhPipeline(object):  # 设置工序一
    wb = Workbook()
    ws = wb.active
    ws.append(['名称', '日期', '链接','编号','招标人','代理机构','招标人电话','代理机构电话','第一中标人','第二中标人','第三中标人','拟中标人','中标金额','限价','工商注册号','组织机构代码',"投诉"])
    def process_item(self, item, spider):  # 工序具体内容
        line = [item['name'], item['date'], item['link'],item['zbbh'],item['zbr'],item['dljg'],item['lxdh1'],item['lxdh2'],item['stzbr'],item['ndzbr'],item['tdzbr'],item['nizbr'],item['je'],item['xj'],item['gszch'],item['zzjgdm'],item['tsbm'],]  # 把数据中每一项整理出来
        self.ws.append(line)  # 将数据以行的形式添加到xlsx中
        self.wb.save('./outcome2.xlsx')  # 保存xlsx文件
        return item