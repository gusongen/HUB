import scrapy


class HhhItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #需要的四个属性
     name = scrapy.Field()
     link = scrapy.Field()
     date = scrapy.Field() 
     details = scrapy.Field() 
     