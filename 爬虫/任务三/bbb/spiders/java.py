import scrapy
import re
from  bbb.items import BbbItem
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument('--headless')


class JavaSpider(scrapy.Spider):
    name = 'java'#蜘蛛名
    allowed_domains = ['cqjsxx.com']
    def start_requests(self):  #用selenium实现翻页，将每页的数据传给parse1解析
        url="http://www1.cqjsxx.com/webcqjg/GcxxFolder/zhongbiao.aspx?tdsourcetag=s_pctim_aiomsg"
        driver = webdriver.Chrome(chrome_options=chrome_options)#以无头模式爬取
        driver.get(url) 
        page=1
        while page<=875:#875#遍历所有页面
            content=driver.page_source

        # self.parse1(content,page)
            sel=scrapy.selector.Selector(text=content)
            a=sel.xpath('//tr//td[1]//a').extract()#xpath+正则得到每页上的中标信息
            b=sel.re("[0-9]{4,4}-[0-9]{2,2}-[0-9]+")
            c=sel.xpath('//td[3]//font').extract()
            d=sel.xpath('//td[2]//font').extract()
            for i in range(0,18):#18
                item=BbbItem()#实例化
                name=re.findall('[\u4e00-\u9fa5]+[^<]*<',a[i])
                name= re.sub("<","",name[0])
                item['name']=name
                link=re.findall('zhongbiao[^"]+"',a[i])
                link=re.sub('"',"",link[0])
                link=re.sub('amp;',"",link)
                link="http://www1.cqjsxx.com/webcqjg/GcxxFolder/"+link
                item['link']=link
                item['date']=b[i]
                item['quyu']=re.sub('<[^<]*>','',c[i+1])
                danwei=re.sub('<[^<]*>','',d[i+2])
                danwei=re.sub(r'\n|\r|\t',"",danwei)
                item['zhonbiaodanwei']=danwei
                yield scrapy.Request(url=link, meta={'item':item} ,callback=self.parse2)
            page+=1
            submit=driver.find_element_by_xpath('//*[@id="Linkbutton3"]')#xpath定位给翻页按钮
            submit.click()#翻页
    def parse2(self,response):
        item =response.meta['item'] 
        sel=scrapy.selector.Selector(response)
        a=sel.xpath('//*[@id="Table3"]').extract() #所有的有用信息均在td或h4标签下，通过xpath得到一个列表
        b=''  #空列表记录合并所有有效信息
        for i in a:#遍历a中的所有元素，通过正则去掉多余部分
            i=re.sub('<[^>]*>',"",i)
            i=re.sub(r'\xa0',"",i)
            i=re.sub(r'\n|\r|\t',"",i)
            i=i.strip()
            if(len(i)!=0 and i.isspace()==False):#排除掉空格或者空的元素
                b+=","+i 
        item['details']=b
        return item

