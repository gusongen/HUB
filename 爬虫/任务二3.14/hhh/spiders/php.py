# -*- coding: utf-8 -*-
import scrapy
import re
from hhh.items import HhhItem
from selenium import webdriver

from selenium.webdriver.chrome.options import Options



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
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver=webdriver.Chrome(chrome_options = chrome_options)
        #driver=webdriver.Chrome()
        url="http://www.fdggzy.cn/lbv3/n_newslist_zz_item.aspx?ILWHBNjF4clKo8UY2fiQHA=="
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
                yield scrapy.Request(url=link, meta={'item':item} ,callback=self.parse)
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
        
   
    '''def parse2(self,response):
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
        return item'''
    def parse(self, response):
        item =response.meta['item'] 
        item['zbbh']=item['zbr']=item['dljg']=item['lxdh1']=item['lxdh2']=item['stzbr']=item['ndzbr']=item['tdzbr']=item['nizbr']=item['je']=item['xj']=item['gszch']=item['zzjgdm']=item['tsbm']=''
        a=response.xpath('//tbody//td//text()').extract()
        b=[]
        ok=1  
        dh=1
        xjf=1
        jef=1
        dyzbr=''
        dezbr=''
        dszbr=''     
        for i in range(len(a)):
            a[i]=a[i].strip()
            if(a[i]=="招"):
                b.append("招标人")
            elif(a[i]=="标" or a[i]=="人" or a[i]=="(" or a[i]==")" or a[i]=="（"  or a[i]=="）" or a[i]=='\xa0' or a[i]=='\xa0 ' or a[i]=="\r\n  " or a[i]=="" or a[i].isspace()):
                pass
            elif(a[i]=="中"):   #有的是'拟中标人'
                b.append("中标人")
            elif ("联系" in a[i]): 
                b.append('联系电话')
            elif (a[i]=='电话' or a[i]=='联系'): 
                pass
            elif(a[i].isdigit() and a[i+1]=='-' and a[i+2].isdigit()):
                b.append(a[i]+a[i+2])
            elif(( "招标人："  in a[i]) or ('公章' in a[i])):
                ok=0
            elif(ok):
                b.append(a[i])    
            else :
                pass
        for i in range(len(b)):
            b[i]=re.sub('\xa0|\n|\r|-','',b[i])
            b[i]=b[i].strip()
            if(i+1<len(b) and b[i]=='-'):
                b[i-1]+=b[i+1]
                b.pop(i+1)
                b.pop(i)
            if(b[i].isspace()or b[i]==''):
                b.pop(i)
        #item=XxxItem()
        
        for i in range(len(b)):
            #确保是第一个联系电话不是投诉电话
            if("编号" in b[i]):
                zbbh=''
                for j in range(3):
                    if(i+j+1<len(b) and (b[i+j+1].isdigit() or re.sub("-|[a-z]|[A-Z]",'',b[i+j+1]).isdigit())):
                        zbbh+=b[i+j+1]
                        zbbh+=' '
                item['zbbh']=zbbh
            elif("招标人" in b[i] or "招 标人" in b[i]):
                item['zbr']=b[i+1]
            elif("中标人" in b[i]):
                item['nizbr']=b[i+1]
            elif("电话"in b[i] and dh):
                dh=0
                item["lxdh1"]=b[i+1]
                if(i+j+1<len(b) and  b[i+4].isdigit()):
                    item["lxdh2"]=b[i+4]
            elif("代理机构"in b[i]):
                item['dljg']=b[i+1]
            elif("第一中标候选人"in b[i]):
                if(not b[i+1].isspace() and not "第二"in b[i+1]):
                    dyzbr+=b[i+1]+' '    #有可能多个标段
            elif("第二中标候选人"in b[i]):
                if(not b[i+1].isspace() and not "第三"in b[i+1]):
                    dezbr+=b[i+1]+' '
            elif("第三中标候选人"in b[i]):
                if(not b[i+1].isspace() and b[i+1]!='中标人' and b[i+1]!='拟中标人' ):
                    dszbr+=b[i+1]+' '
            elif('金额' in b[i] and jef):
                dw=""
                if('万'in b[i] and '元' in b[i]):
                    dw="万元"
                elif('元' in b[i]):
                    dw='元'
                for j in range(len(b)-i):
                    if (i+j+2<len(b) and  '元'in b[i+j+1] and re.sub('\.','',b[i+j+2]).isdigit()):
                        item["je"]=b[i+j+2]+b[i+j+1]
                        jef=0
                        b[i+j+2]=''
                        b[i+j+1]=''
                    elif(i+j+2<len(b) and  '元'in b[i+j+2] and re.sub('\.','',b[i+j+1]).isdigit()):
                        item["je"]=b[i+j+1]+b[i+j+2]
                        jef=0
                        b[i+j+1]=''
                        b[i+j+2]=''
                    elif(i+j+1<len(b) and  '元'in b[i+j+1]and re.sub('\.|元|万','',b[i+j+1]).isdigit()):
                        item["je"]=b[i+j+1]
                        jef=0
                        b[i+j+1]=''
                    elif(i+j+1<len(b) and  "."in b[i+j+1] and re.sub('\.|[\u4e00-\u9fa5]','',b[i+j+1]).isdigit()):
                        item["je"]=b[i+j+1]+dw
                        jef=0
                        b[i+j+1]=''
            elif('限价' in b[i] and xjf):
                dw=""
                if('万'in b[i] and '元' in b[i]):
                    dw="万元"
                elif('元' in b[i]):
                    dw='元'
                if('元'in b[i+1] and re.sub('\.','',b[i+2]).isdigit()):
                    item["xj"]=b[i+2]+b[i+1]
                    xjf=0
                elif('元'in b[i+2] and re.sub('\.','',b[i+1]).isdigit()):
                    item["xj"]=b[i+1]+b[i+2]
                    xjf=0
                elif('元'in b[i+1]):
                    item["xj"]=b[i+1]
                    xjf=0
                elif(re.sub('\.','',b[i+1]).isdigit()):
                    item["xj"]=b[i+1]
                    xjf=0
            elif("中标人"in b[i]):
                item['']=b[i+1]
            elif("注册号"in b[i] ): 
                item['gszch']=b[i+1]
            elif(("机构代码"in b[i] or "信用代码"in b[i] )and b[i+1].isalnum()): #两码是一个
                item['zzjgdm']=b[i+1]
            elif("投诉受理"in b[i]):
                tssl=""
                for j in range(1,len(b)-i):
                    if("联" not in b[i+j] and "系" not in b[i+j] and "电" not in b[i+j] and "话" not in b[i+j] and "部门" not in b[i+j] ):
                        tssl+=b[i+j]+' '
                item['tsbm']=tssl
            item['stzbr']=dyzbr
            item['ndzbr']=dezbr
            item['tdzbr']=dszbr
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
        

