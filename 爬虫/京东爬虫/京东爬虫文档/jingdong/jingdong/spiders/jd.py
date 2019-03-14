# -*- coding: utf-8 -*-
import scrapy
import pdb#这个是pdb模块，可以给py加入间断点。我们可以通过pdb.set_trace()来调试我们的py是否出现问题
from scrapy.http import Request#使用Request需要用到的模块
from jingdong.items import JingdongItem#导入在items.py中定义的
import re#导入正则模块
import sys#下三行都是为了让爬下来的数据编码变成utf-8
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib2#导入抓包时需要的模块（打开页面需要）


class JdSpider(scrapy.Spider):#方法前的都是创建py时自动生成
	name = "jd"
	allowed_domains = ["jd.com"]
	start_urls = (
        'http://www.jd.com/',#起始页面
    )

	def parse(self, response):#在爬虫中，进入几层网页便需要几个函数
		#pdb.set_trace()
		key="零食"#搜索字符
		for i in range(0,100):
			#pdb.set_trace()
			url="http://search.jd.com/Search?keyword="+str(key)+"&enc=utf-8&wq="+str(key)+"&page="+str(2*i+1)#在文档中提到过，这个网站的规律是1,3,5,7,8所以按照这个规律利用for循环依次进入
			#print(url)
			yield Request(url=url,callback=self.page)#不断申请上面网页，申请完后，进入下个函数
	
	def page(self,response):
		#print response.url
		#pdb.set_trace()
		number=response.xpath('//li')#这是商品编号，利用xpath表达式从页面源代码中将所有商品编码提取出来
		for i in number:
			#pdb.set_trace()
			allid=i.xpath('@data-sku').extract()#然后利用for循环，将所有商品编码变成list
			print(allid)
		#item=JingdongItem()
		#pdb.set_trace()
		#item['price']=response.xpath('//div[@class="p-price"]/strong[@data-price]/i/text()').extract()
		#yield item	
		for j in range(0,len(allid)):
			thisid=allid[j]
			url1='https://item.jd.com/'+str(thisid)+'.html'#利用for循环商品number，陪凑商品网页
			#pdb.set_trace()
			yield Request(url=url1,callback=self.next)#和上面一样，申请网页然后进入下个函数
	def next(self,response):
		item=JingdongItem()
		#pdb.set_trace()
		item['title']=response.xpath('//div[@id="name"]/h1/text()').extract()#将提取到的东西放入items.py，下面也是一样
		#print item['title']
		item['link']=response.url
		ZZ_P='[0-9]{1,20}'#这是一个正则，匹配商品编码（由于反爬机制，源代码中不存在价格，所以以抓包的形式获取）
		ID= re.compile(ZZ_P).findall(item['link'])[0]#就是指从所有的链接中匹配商品编码
		item['number']=ID
		p_price='https://p.3.cn/prices/get?type=1&area=1_72_2799&pdtk=&pduid=653872602&pdpin=&pdbp=0&skuid=J_'+str(ID)#这是利用浏览器抓包后获得的网址，再配合商品编码得到每一个包（可以看一下settings.py）
		temp=urllib2.urlopen(p_price).read().decode("utf-8","ignore")#利用urllib2中的打开网页的方法，再将其转化为utf-8编码
		ZZ_P2 = '"p":"(.*?)"'#匹配价格的正则
		item['price'] = re.compile(ZZ_P2).findall(temp)#匹配出价格
		item['pic_url']='https://item.jd.com/bigimage.aspx?id='+str(ID)#这是商品图片的网址
		yield item


		

		
		
		
			
		

	
		
			
        
