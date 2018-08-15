# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ElbaladItem(scrapy.Item):

    title = scrapy.Field()
    content = scrapy.Field()



class LongXunDaoHang(scrapy.Item):
    # 分类link
    categoryLink = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()