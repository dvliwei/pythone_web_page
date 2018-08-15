# -*- coding: utf-8 -*-

import scrapy
import re
from scrapy.spider import Request

#crawlspider,rule配合使用可以起到遍历全站的作用，request为请求的接口

from scrapy.spider import CrawlSpider,Rule
#配合使用Rule进行url规则匹配
from scrapy.linkextractors import LinkExtractor

from elbalad.items import LongXunDaoHang

class longxunDaoHang(CrawlSpider):
    name = 'longxun'
    allowed_domains = ['elbalad.news']

    start_urls = ['https://www.elbalad.news/']

    rules = (
        Rule(LinkExtractor(allow=('\.news\/*',)), callback='parse_item', follow=True),
        #Rule(LinkExtractor(allow=('\.news\/[0-9]+') ,restrict_xpaths=("//div[@class='post-cont']")),
        # callback="parse_item",follow=True),
        #Rule(LinkExtractor(allow=('\.news\/show\.aspx\?id=[0-9]+'),restrict_xpaths=("//div[@class='post-cont']")),
        # callback="parse_item",follow=True),
    )

    def parse_item(self, response):

        daohang = LongXunDaoHang()
        daohang['categoryLink'] = response.url

        title_str = response.xpath('//title/text()')
        content_str = response.xpath("//div[@class='post-cont']")
        if content_str and title_str:
           content = re.sub(r'</?\w+[^>]*>', '', content_str.extract()[0])
           daohang['title'] = title_str.extract()[0]
           daohang['content'] = content


        yield daohang