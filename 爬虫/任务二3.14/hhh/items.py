import scrapy


class HhhItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #需要的四个属性
     name = scrapy.Field()
     link = scrapy.Field()
     date = scrapy.Field() 
     #details = scrapy.Field() 
     zbbh=scrapy.Field()  #标号
     zbr=scrapy.Field()   #招标人
     dljg=scrapy.Field()  #代理机构
     lxdh1=scrapy.Field()  #招标人电话
     lxdh2=scrapy.Field()  #代理电话
     stzbr=scrapy.Field()  #第一中标人
     ndzbr=scrapy.Field()#第二
     tdzbr=scrapy.Field()#第三
     nizbr=scrapy.Field()#拟中标
     je=scrapy.Field()#金额
     gszch=scrapy.Field()# 工商注册号
     zzjgdm=scrapy.Field()#组织机构代码
     tsbm=scrapy.Field() #投诉部门
     xj=scrapy.Field()
     