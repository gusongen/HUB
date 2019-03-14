# -*- coding: utf-8 -*-
from scrapy import Request,Spider
import scrapy
from urllib.parse import quote
from ss.items  import  SsItem
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from scrapy.http import HtmlResponse
from logging import getLogger
import re



class SSpider(Spider):
    name = 's'
    allowed_domains = ['http://www.fdggzy.cn']
    base_urls = ['http://www.fdggzy.cn/']
    
    browser=webdriver.Chrome()
    wait =WebDriverWait(browser,10)
    MAX_PAGE = 80
    for i in range(1,MAX_PAGE+1):
        index_page(i)
     
    def index_page(self,page):
        print("正在爬取第",page,"页")
        try:
            url="http://www.fdggzy.cn/lbv3/n_newslist_zz_item.aspx?ILWHBNjF4clKo8UY2fiQHA=%3d"
            browser.get(url)
            if page>1:
                submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#ctl00_ContentPlaceHolder2_F3")))
                submit.click()

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#ctl00_ContentPlaceHolder2_DataList1 > tbody > tr"))) 
            get_it()
        
    def parse(self, response):   #得到包中的url和日期以及名称
        sel=scrapy.selector.Selector(response)
        htmls=sel.re("/jyjg[^(\")]*.html")  #正则得到url的部分
        names=sel.re(r'title\\":\\"[^\\"]*')   #正则得到名称部分
        dates= sel.re(r'infodate\\":\\"[^\\"]*')   #正则得到日期
        
        for i in range(0,len(htmls)):#遍历所有的url

            htmls[i]="https://www.cqggzy.com"+re.sub(r'\\/',"/",htmls[i]) #url拼接
            names[i]=re.sub(r'title\\":\\"',"",names[i])  #正则替换掉名称中的多余部分
            dates[i]=re.sub(r'infodate\\":\\"',"",dates[i]) #正则替换掉日期中的多余部分
            item=SsItem()  #实例化item类
            item['link']= htmls[i]  #写入item的属性
            item['date']= dates[i]  
            item['name']= names[i]
            yield scrapy.Request(url=htmls[i], meta={'item':item} ,callback=self.parse1)#将得到的链接传入下一个parse中解析
            
        
    
    def parse1(self,response):
        item =response.meta['item'] 
        sel=scrapy.selector.Selector(response)
        a=sel.xpath('//td|//h4').extract() #所有的有用信息均在td或h4标签下，通过xpath得到一个列表
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

