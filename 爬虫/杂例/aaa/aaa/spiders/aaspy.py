# -*- coding: utf-8 -*-
import scrapy
import re
from  aaa.items import AaaItem
from  aaa.middlewares import SeleniumMiddleware

class AaspySpider(scrapy.Spider):
    name = 'aaspy'
    allowed_domains = ['fdggzy.cn']
    start_urls = 'http://www.fdggzy.cn/lbv3/n_newslist_zz_item.aspx?ILWHBNjF4clKo8UY2fiQHA=%3d'
    
    def start_requests(self):
        for page in range(1,self.settings.get('MAX_PAGE')+1):
          url=self.start_urls
          yield scrapy.Request(url=url,callback=self.parse,meta={'page':page},dont_filter=True)
    
    def parse(self, response):   #得到包中的url和日期以及名称
        sel=scrapy.selector.Selector(response)
        a=sel.xpath('//*[@id="ctl00_ContentPlaceHolder2_DataList1"]//a').extract()
        b=sel.re("[0-9]*-[0-9]*-[0-9]*")
            
        for i in range(0,20):
          item=AaaItem()
          item['name']=re.sub("<[^>]*>","",a[i])
          link=re.sub('<a[^"]*"',"",a[i])
          link="http://www.fdggzy.cn/lbv3/"+re.sub('" n>(.)*',"",link)
          item['link']=link
          item['date']=b[i]
          yield scrapy.Request(url=link, meta={'item':item} ,callback=self.parse1)
         
    def parse1(self,response):
        item =response.meta['item'] 
        sel=scrapy.selector.Selector(response)
        a=sel.xpath('//tbody//td').extract() #所有的有用信息均在td或h4标签下，通过xpath得到一个列表
        b=[]  #空列表记录合并所有有效信息
        for i in a:#遍历a中的所有元素，通过正则去掉多余部分
            i=re.sub('<[^>]*>',"",i)
            i=re.sub(r'\xa0',"",i)
            i=re.sub(r'\n|\r',"",i)
            i=i.strip()
            if(len(i)!=0 and i.isspace()==False):#排除掉空格或者空的元素
              b.append(i) 
        item['details']=b
        return item

        
