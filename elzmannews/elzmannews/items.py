# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ElzmannewsItem(scrapy.Item):
    url = scrapy.Field()
    page_name = scrapy.Field()
    do_main = scrapy.Field()
    str_size = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()