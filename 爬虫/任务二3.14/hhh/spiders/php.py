# -*- coding: utf-8 -*-
import scrapy
import re
from hhh.items import HhhItem
from selenium import webdriver


class PhpSpider(scrapy.Spider): #需要继承scrapy.Spider类
    name = "php" # 定义蜘蛛名
    allowed_domains=["cqggzy.com"]
    
    ''' unicornHeader = {
        'Host': 'www.fdggzy.cn',
        'Connection': 'keep-alive',
        'Content-Length':'10000',
        'Cache-Control':' max-age=0',
        'Origin': 'http://www.fdggzy.cn',
        'Upgrade-Insecure-Requests':' 1',
        'Content-Type':' application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
        'Accept':' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer':' http://www.fdggzy.cn/lbv3/n_newslist_zz_item.aspx?ILWHBNjF4clKo8UY2fiQHA=%3d',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'safedog-flow-item=; ASP.NET_SessionId=zqpphd1xpfohjtvss3vzzu1f'
        }

# 表单需要提交的数据
    myFormData = {
'__EVENTTARGET': '',
'__EVENTARGUMENT': '',
'__VIEWSTATE':'',
'__EVENTVALIDATION': '',
'ctl00$n_search1$searchBox': '',
'ctl00$ContentPlaceHolder2$TextBox1': '',
'ctl00$ContentPlaceHolder2$TextBox2': '',
'ctl00$ContentPlaceHolder2$TextBox3':'', 
'ctl00$ContentPlaceHolder2$T1': '',
'ctl00$ContentPlaceHolder2$T2':' 1',
'ctl00$ContentPlaceHolder2$F3':' 下一页'}'''
    


    
    def start_requests(self):
        url="http://www.fdggzy.cn/lbv3/n_newslist_zz_item.aspx?ILWHBNjF4clKo8UY2fiQHA=="
        driver=webdriver.Chrome()
        driver.get(url) 
        page=1
        while page<=81:#81
            content=driver.page_source

           # self.parse1(content,page)
            sel=scrapy.selector.Selector(text=content)
            a=sel.xpath('//*[@id="ctl00_ContentPlaceHolder2_DataList1"]//a').extract()
            b=sel.re("[0-9]+-[0-9]+-[0-9]+")
            for i in range(0,20):#20
                item=HhhItem()
                item['name']=re.sub("<[^>]*>","",a[i])
                link=re.sub('<a[^"]*"',"",a[i])
                link=re.sub('" (.)*>',"",link)
                
                link="http://www.fdggzy.cn/lbv3/"+link
                item['link']=link
                item['date']=b[i]
                yield scrapy.Request(url=link, meta={'item':item} ,callback=self.parse2)



            page+=1
            submit=driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder2_F3"]')
            submit.click()
        

            """vs=sel.xpath('//input[@id="__VIEWSTATE"]').extract()
            a=re.findall('[^"]*\+[^"]*',vs[0])
            self.myFormData['__VIEWSTATE']=a[0]
            vss=sel.xpath('//input[@id="__EVENTVALIDATION"]').extract()
            b=re.findall('[^"]*\+[^"]*',vss[0])
            self.myFormData['__EVENTVALIDATION']=b[0]
            yield scrapy.FormRequest(url = "http://www.fdggzy.cn/lbv3/n_newslist_zz_item.aspx?ILWHBNjF4clKo8UY2fiQHA=%3d",
            headers = self.unicornHeader,
            method = 'POST',             # GET or POST
            formdata = self.myFormData,       # 表单提交的数据
            dont_filter = True     
            )"""

        
        
    #def parse1(self, content,page):   #得到包中的url和日期以及名称
        
   
    def parse2(self,response):
        item =response.meta['item'] 
        sel=scrapy.selector.Selector(response)
        a=sel.xpath('//tbody//td').extract() #所有的有用信息均在td或h4标签下，通过xpath得到一个列表
        b=''  #空列表记录合并所有有效信息
        for i in a:#遍历a中的所有元素，通过正则去掉多余部分
            i=re.sub('<[^>]*>',"",i)
            i=re.sub(r'\xa0',"",i)
            i=re.sub(r'\n|\r',"",i)
            i=i.strip()
            if(len(i)!=0 and i.isspace()==False):#排除掉空格或者空的元素
              b+=","+i 
        item['details']=b
        return item

     
        #'''  def parse(self, response):   #得到包中的url和日期以及名称
        #sel=scrapy.selector.Selector(response)
    #htmls=sel.re("/jyjg[^(\")]*.html")  #正则得到url的部分
        #names=sel.re(r'title\\":\\"[^\\"]*')   #正则得到名称部分
        #dates= sel.re(r'infodate\\":\\"[^\\"]*')   #正则得到日期
        
       # for i in range(0,len(htmls)):#遍历所有的url

        ##   names[i]=re.sub(r'title\\":\\"',"",names[i])  #正则替换掉名称中的多余部分
          #  dates[i]=re.sub(r'infodate\\":\\"',"",dates[i]) #正则替换掉日期中的多余部分
           # item=HhhItem()  #实例化item类
            #item['link']= htmls[i]  #写入item的属性
            #item['date']= dates[i]  
          #  item['name']= names[i]
          #  yield scrapy.Request(url=htmls[i], meta={'item':item} ,callback=self.parse1)#将得到的链接传入下一个parse中解析
            
        

   # def parse1(self,response):
    #    item =response.meta['item'] 
     #   sel=scrapy.selector.Selector(response)
     ###   a=sel.xpath('//td|//h4').extract() #所有的有用信息均在td或h4标签下，通过xpath得到一个列表
      #  b=[]  #空列表记录合并所有有效信息
      #  for i in a:#遍历a中的所有元素，通过正则去掉多余部分
       #     i=re.sub('<[^>]*>',"",i)
        #    i=re.sub(r'\xa0',"",i)
         #   i=re.sub(r'\n|\r',"",i)
          #  i=i.strip()
           # if(len(i)!=0 and i.isspace()==False):#排除掉空格或者空的元素
           #     b.append(i) 
       # item['details']=b
       # return item'''
        

