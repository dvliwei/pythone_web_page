# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import time
from twisted.enterprise import  adbapi
from scrapy.conf import settings
import pymongo

class MasrawyPipeline(object):
    def process_item(self, item, spider):
        return item

# 写入json文件
class JsonWritePipline(object):
    def __init__(self):#定义全局

        self.logfilename = 'json/mas_' + time.strftime("%Y%m%d", time.localtime()) + '.log'
    def process_item(self,item,spider):

        self.filename = 'json/mas_' + time.strftime("%Y%m%d%H", time.localtime()) + '.json'
        if 'title' in item:
            nItem = dict(item)
            del nItem['url']
            del nItem['page_name']
            del nItem['str_size']
            del nItem['do_main']
            line = json.dumps(nItem) + "\n"
            with open(self.filename, 'a+') as f:
                f.writelines(line)
            pass

        line = json.dumps(dict(item)['url']) + "\n"
        with open(self.logfilename, 'a+') as f:
            f.writelines(line)
        pass

        return item

    # def spider_closed(self,spider):
    #     self.file.close()



class MongoPipeline(object):

    def __init__(self):
        host=settings["MONGODB_HOST"]
        port=settings["MONGODB_PORT"]
        dbname=settings["MONGODB_DBNAME"]
        sheetname=settings["MONGODB_SHEETNAME"]
        # 创建MONGODB数据库链接
        client=pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        mydb=client[dbname]
        # 存放数据的数据库表名
        self.post=mydb[sheetname]

    def process_item(self, item, spider):


        if 'str_size' in item:
            data = dict(item)
            del data['title']
            del data['content']
            self.post.insert(data)
        return item