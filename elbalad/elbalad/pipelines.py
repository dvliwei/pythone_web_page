# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import io
import time
class ElbaladPipeline(object):
    def process_item(self, item, spider):
        return item
# 写入json文件
class JsonWritePipline(object):
    def __init__(self):
        self.file = io.open('elbaladurl.json','a+',encoding='utf-8')

        self.filename = 'json/' + time.strftime("%Y%m%d%H", time.localtime()) + '.json'
        self.logfilename = 'json/' + time.strftime("%Y%m%d", time.localtime()) + '.log'
    def process_item(self,item,spider):


        if 'title' in item:
            nItem = dict(item)
            del nItem['categoryLink']
            line = json.dumps(nItem) + "\n"
            with open(self.filename, 'a+') as f:
                f.writelines(line)
            pass

        line = json.dumps(dict(item)['categoryLink']) + "\n"
        with open(self.logfilename, 'a+') as f:
            f.writelines(line)
        pass

        return item

    # def spider_closed(self,spider):
    #     self.file.close()