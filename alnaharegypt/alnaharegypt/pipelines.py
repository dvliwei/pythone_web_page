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


class AlnaharegyptPipeline(object):
    def process_item(self, item, spider):
        return item


# 写入json文件
class JsonWritePipline(object):
    def __init__(self):#定义全局

        self.logfilename = 'json/alna_' + time.strftime("%Y%m%d", time.localtime()) + '.log'
    def process_item(self,item,spider):

        self.filename = 'json/alna_' + time.strftime("%Y%m%d%H", time.localtime()) + '.json'
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



# class WebcrawlerScrapyPipeline(object):
#     '''保存到数据库中对应的class
#          1、在settings.py文件中配置
#          2、在自己实现的爬虫类中yield item,会自动执行'''
#
#     def __init__(self, dbpool):
#         self.dbpool = dbpool
#
#     @classmethod
#     def from_settings(cls, settings):
#         '''1、@classmethod声明一个类方法，而对于平常我们见到的叫做实例方法。
#            2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
#            3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
#         # 读取settings中配置的数据库参数
#         dbparams = dict(
#             host=settings['MYSQL_HOST'],
#             db=settings['MYSQL_DBNAME'],
#             user=settings['MYSQL_USER'],
#             passwd=settings['MYSQL_PASSWD'],
#             charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
#             cursorclass=MySQLdb.cursors.DictCursor,
#             use_unicode=False,
#         )
#         dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
#         return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到
#
#     # pipeline默认调用
#     def process_item(self, item, spider):
#         query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
#         query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
#         return item
#
#     # 写入数据库中
#     # SQL语句在这里
#     def _conditional_insert(self, tx, item):
#         sql = "insert into alna_page_urls(page_name,do_main,url,str_size,created_at) values(%s,%s,%s,%s,%s)"
#         params = (
#         item['page_name'], item['do_main'], item['url'], item['str_size'], time.strftime("%Y-%m-%d %H:%M%S",time.localtime()))
#         tx.execute(sql, params)
#
#     # 错误处理方法
#     def _handle_error(self, failue, item, spider):
#         print failue



