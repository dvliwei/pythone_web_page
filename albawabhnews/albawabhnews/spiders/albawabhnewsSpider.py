# -*- coding: utf-8 -*-

import scrapy
import re
from scrapy.spider import Request
import  hashlib
import time
#crawlspider,rule配合使用可以起到遍历全站的作用，request为请求的接口

from scrapy.spider import CrawlSpider,Rule
#配合使用Rule进行url规则匹配
from scrapy.linkextractors import LinkExtractor
from albawabhnews.items import AlbawabhnewsItem
from bs4 import  BeautifulSoup
from selenium import webdriver

class albawabhnewsSpider(CrawlSpider):
    name = 'albawabhnews'
    allowed_domains = ['albawabhnews.com']

    start_urls = ['http://www.albawabhnews.com/']

    rules = (
        Rule(LinkExtractor(allow=('\.albawabhnews\.com\/.*',)), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=('\.news\/[0-9]+') ,restrict_xpaths=("//div[@class='post-cont']")),
        # callback="parse_item",follow=True),
        # Rule(LinkExtractor(allow=('\.news\/show\.aspx\?id=[0-9]+'),restrict_xpaths=("//div[@class='post-cont']")),
        # callback="parse_item",follow=True),
    )


    def parse_item(self, response):

        m2 = hashlib.md5()
        m2.update(response.url)

        alba = AlbawabhnewsItem()
        alba['url'] = response.url
        alba['page_name'] = m2.hexdigest()
        alba['do_main'] = 'albawabhnews.com'

        title_str = response.xpath('//title/text()')
        #content_str = response.xpath("//div[@id='show-parags']//div[@class='ni-content']/text()")
        # type_str = response.xpath('//div[@id="PressH"]/b') #分类

        if  title_str:
            content = ""
            # for s in content_str.extract():
            #     content += s

            alba['title'] = title_str.extract()[0]
            alba['content'] = content
            alba['str_size'] = len(content)

        # 分享页
        # content_str_y = response.xpath('//div[@id="content"]/div[@id="TPKcnt"]/p')
        # if content_str_y and title_str:
        #     content = re.sub(r'</?\w+[^>]*>', '', content_str_y.extract()[0])
        #     alna['title'] = title_str.extract()[0]
        #     alna['content'] = content
        #     alna['str_size'] = len(content)

        yield alba

