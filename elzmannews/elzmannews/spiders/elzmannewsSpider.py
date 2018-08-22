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

from elzmannews.items import  ElzmannewsItem

class elzmannewsSpider(CrawlSpider):
    name = 'elzm'
    allowed_domains = ['elzmannews.com']

    start_urls = ['https://www.elzmannews.com']

    rules = (
        Rule(LinkExtractor(allow=('\.elzmannews\.com\/.*',)), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=('\.news\/[0-9]+') ,restrict_xpaths=("//div[@class='post-cont']")),
        # callback="parse_item",follow=True),
        # Rule(LinkExtractor(allow=('\.news\/show\.aspx\?id=[0-9]+'),restrict_xpaths=("//div[@class='post-cont']")),
        # callback="parse_item",follow=True),
    )

    def parse_item(self, response):
        elzm = ElzmannewsItem()

        if 'javascript:ajxpg' in response.body:
            attr = re.search('javascript:ajxpg\(\'[^\']+', response.body).span()
            elzm['url'] = 'https://www.elzmannews.com/' + response.body[attr[0] + 18: attr[1]] +'&'+ str(int(time.time())*1000);
            yield elzm

        m2 = hashlib.md5()
        m2.update(response.url)

        elzm['url'] = response.url
        elzm['page_name'] = m2.hexdigest()
        elzm['do_main'] = 'elzmannews.com'

        title_str = response.xpath('//title/text()')
        content_str = response.xpath("//div[@id='sBDY']/article//p/text()")
        # type_str = response.xpath('//div[@id="PressH"]/b') #分类

        if content_str and title_str:
            content = ""
            for s in content_str.extract():
                content += s

            elzm['title'] = title_str.extract()[0]
            elzm['content'] = content
            elzm['str_size'] = len(content)

        # 分享页
        # content_str_y = response.xpath('//div[@id="content"]/div[@id="TPKcnt"]/p')
        # if content_str_y and title_str:
        #     content = re.sub(r'</?\w+[^>]*>', '', content_str_y.extract()[0])
        #     alna['title'] = title_str.extract()[0]
        #     alna['content'] = content
        #     alna['str_size'] = len(content)

        yield elzm