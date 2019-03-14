import scrapy
import re
from  sss.items import SssItem

class SssSpider(scrapy.Spider): #需要继承scrapy.Spider类
    name = "sss" # 定义蜘蛛名
    allowed_domains=["cqggzy.com"]
    def start_requests(self): # 抓包
       yield scrapy.Request(url="https://www.cqggzy.com/web/services/PortalsWebservice/getInfoList?response=application/json&pageIndex=1&pageSize=7&siteguid=d7878853-1c74-4913-ab15-1d72b70ff5e7&categorynum=005&title=&infoC=&_=1549949026164", callback=self.parse) #爬取到的页面如何处理？提交给parse方法处理
    
    def parse(self, response):   #得到包中的url和日期以及名称
        sel=scrapy.selector.Selector(response)
        htmls=sel.re("/jyjg[^(\")]*.html")  #正则得到url的部分
        names=sel.re(r'title\\":\\"[^\\"]*')   #正则得到名称部分
        dates= sel.re(r'infodate\\":\\"[^\\"]*')   #正则得到日期
        
        for i in range(0,len(htmls)):#遍历所有的url

            htmls[i]="https://www.cqggzy.com"+re.sub(r'\\/',"/",htmls[i]) #url拼接
            names[i]=re.sub(r'title\\":\\"',"",names[i])  #正则替换掉名称中的多余部分
            dates[i]=re.sub(r'infodate\\":\\"',"",dates[i]) #正则替换掉日期中的多余部分
            item=SssItem()  #实例化item类
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

