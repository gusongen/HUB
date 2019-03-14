
#将得到item写入json
import json

class SssPipeline(object):
     def __init__(self):
         self.filename=open("outcome.json","wb")
     def process_item(self, item, spider):
         jsontext=json.dumps(dict(item),ensure_ascii=False) + ",\n"
         self.filename.write(jsontext.encode("utf-8"))#防止乱码！！！
         return item
     def close_spider(self,spider):
           self.filename.close()