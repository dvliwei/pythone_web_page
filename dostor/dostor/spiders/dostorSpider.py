# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#http://www.elfagr.com/ 网站深度采集
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import scrapy
import re
from scrapy.spider import Request
import  hashlib
import time
#crawlspider,rule配合使用可以起到遍历全站的作用，request为请求的接口

from scrapy.spider import CrawlSpider,Rule
#配合使用Rule进行url规则匹配
from scrapy.linkextractors import LinkExtractor

from dostor.items import  DostorItem

class dostorSpider(CrawlSpider):
    name = 'dostor'
    allowed_domains = ['dostor.org']

    start_urls = ['https://www.dostor.org/']

    rules = (
        Rule(LinkExtractor(allow=('\.dostor\.org\/.*',)), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=('\.news\/[0-9]+') ,restrict_xpaths=("//div[@class='post-cont']")),
        # callback="parse_item",follow=True),
        # Rule(LinkExtractor(allow=('\.news\/show\.aspx\?id=[0-9]+'),restrict_xpaths=("//div[@class='post-cont']")),
        # callback="parse_item",follow=True),
    )

    def parse_item(self, response):
        dostor = DostorItem()

        m2 = hashlib.md5()
        m2.update(response.url)

        dostor['url'] = response.url
        dostor['page_name'] = m2.hexdigest()
        dostor['do_main'] = 'dostor.org'

        title_str = response.xpath('//title/text()')
        content_str = response.xpath("//div[@class='post']//div[@class='ni-content']//p/text()")
        # type_str = response.xpath('//div[@id="PressH"]/b') #分类

        if content_str and title_str:
            content = ""
            for s in content_str.extract():
                content += s

            dostor['title'] = title_str.extract()[0]
            dostor['content'] = content
            dostor['str_size'] = len(content)

        # 分享页
        # content_str_y = response.xpath('//div[@id="content"]/div[@id="TPKcnt"]/p')
        # if content_str_y and title_str:
        #     content = re.sub(r'</?\w+[^>]*>', '', content_str_y.extract()[0])
        #     alna['title'] = title_str.extract()[0]
        #     alna['content'] = content
        #     alna['str_size'] = len(content)

        yield dostor