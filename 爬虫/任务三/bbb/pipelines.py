# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from openpyxl import Workbook

class  BbbPipeline(object):  # 设置工序一
    wb = Workbook()
    ws = wb.active
    ws.append(['名称', '日期','区域','中标单位', '详情','链接'])  # 设置表头


    def process_item(self, item, spider):  # 工序具体内容
        line = [item['name'], item['date'],item['quyu'],item['zhonbiaodanwei'], item['details'], item['link']]  # 把数据中每一项整理出来
        self.ws.append(line)  # 将数据以行的形式添加到xlsx中
        self.wb.save('./outcome.xlsx')  # 保存xlsx文件
        return item