# -*- coding: utf-8 -*-

import scrapy
import re
from scrapy.spider import Request
import  hashlib

#crawlspider,rule配合使用可以起到遍历全站的作用，request为请求的接口

from scrapy.spider import CrawlSpider,Rule
#配合使用Rule进行url规则匹配
from scrapy.linkextractors import LinkExtractor

from alnaharegypt.items import AlnaharegyptItem

class alnaSpider(CrawlSpider):
    name = 'alna'
    allowed_domains = ['alnaharegypt.com']

    start_urls = ['http://www.alnaharegypt.com/']

    rules = (
        Rule(LinkExtractor(allow=('\.alnaharegypt\.com\/.*',)), callback='parse_item', follow=True),
        #Rule(LinkExtractor(allow=('\.news\/[0-9]+') ,restrict_xpaths=("//div[@class='post-cont']")),
        # callback="parse_item",follow=True),
        #Rule(LinkExtractor(allow=('\.news\/show\.aspx\?id=[0-9]+'),restrict_xpaths=("//div[@class='post-cont']")),
        # callback="parse_item",follow=True),
    )

    def parse_item(self, response):

        m2 = hashlib.md5()
        m2.update(response.url)

        alna = AlnaharegyptItem()
        alna['url'] = response.url
        alna['page_name'] = m2.hexdigest()
        alna['do_main'] = 'alnaharegypt.com'

        title_str = response.xpath('//title/text()')
        content_str = response.xpath("//div[@id='PressRContent']/p/text()")
        #type_str = response.xpath('//div[@id="PressH"]/b') #分类


        if content_str and title_str:
           content=""
           for s in content_str.extract():
               content+=s

           alna['title'] = title_str.extract()[0]
           alna['content'] = content
           alna['str_size'] = len(content)


        #分享页
        # content_str_y = response.xpath('//div[@id="content"]/div[@id="TPKcnt"]/p')
        # if content_str_y and title_str:
        #     content = re.sub(r'</?\w+[^>]*>', '', content_str_y.extract()[0])
        #     alna['title'] = title_str.extract()[0]
        #     alna['content'] = content
        #     alna['str_size'] = len(content)


        yield alna