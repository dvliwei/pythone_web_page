# -*- coding: utf-8 -*-

import scrapy
import re
from scrapy.spider import Request
import  hashlib

#crawlspider,rule配合使用可以起到遍历全站的作用，request为请求的接口

from scrapy.spider import CrawlSpider,Rule
#配合使用Rule进行url规则匹配
from scrapy.linkextractors import LinkExtractor

from youm7.items import  Youm7Item

class youmSpider(CrawlSpider):
    name = 'youm7'
    allowed_domains = ['youm7.com']

    start_urls = ['https://www.youm7.com/story/2011/4/18/%D8%AA%D8%A7%D9%85%D8%B1-%D8%B9%D8%A7%D8%B4%D9%88%D8%B1-%D9%8A%D8%B1%D9%81%D8%B6-%D8%A7%D9%84%D8%B5%D9%84%D8%AD-%D9%85%D8%B9-%D9%85%D8%B3%D8%A6%D9%88%D9%84%D9%89-%D8%B1%D9%88%D8%AA%D8%A7%D9%86%D8%A7/393728']

    rules = (
        Rule(LinkExtractor(allow=('\.youm7\.com\/.*',)), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=('\.news\/[0-9]+') ,restrict_xpaths=("//div[@class='post-cont']")),
        # callback="parse_item",follow=True),
        # Rule(LinkExtractor(allow=('\.news\/show\.aspx\?id=[0-9]+'),restrict_xpaths=("//div[@class='post-cont']")),
        # callback="parse_item",follow=True),
    )

    def parse_item(self, response):

        m2 = hashlib.md5()
        m2.update(response.url)

        youm = Youm7Item()
        youm['url'] = response.url
        youm['page_name'] = m2.hexdigest()
        youm['do_main'] = 'youm7.com'

        title_str = response.xpath('//title/text()')
        content_str = response.xpath('//article//div[@id="articleBody"]')
        type_str = response.xpath('//article//div[@class="articleHeader"]//div[@class="breadcumb"]//a/text()')#菜单中的分类
        if not type_str:
            type_str = response.xpath('//article//div[@id="articleHeader"]//div[@class="breadcumb"]//a/text()')  # 菜单中的分类
        if content_str and title_str:
            content = ""


            content_str = response.xpath('//article//div[@class="articleCont"]//div[@id="articleBody"]/text()')
            for s in content_str.extract():
                content += s

            content_str = response.xpath('//article//div[@id="articleBody"]//p/text()')
            for s in content_str.extract():
                content += s


            content_str = response.xpath('//article//div[@class="articleCont"]//div[@id="articleBody"]//p//strong/text()')
            for s in content_str.extract():
                content += s

            content_str =response.xpath('//article//div[@id="articleBody"]//div[@dir="auto"]//div/text()')
            for s in content_str.extract():
                content += s

            content_str =response.xpath('//article//div[@id="articleBody"]//div/text()')
            for s in content_str.extract():
                content += s

            # content_str = response.xpath('//article//div[@id="articleBody"]//p/text()')
            # for s in content_str.extract():
            #     content += s

            youm['title'] = title_str.extract()[0]
            youm['content'] = content
            youm['str_size'] = len(content)
            youm['type'] = type_str.extract()[1] #取详细页中的分类

        # 分享页
        # content_str_y = response.xpath('//div[@id="content"]/div[@id="TPKcnt"]/p')
        # if content_str_y and title_str:
        #     content = re.sub(r'</?\w+[^>]*>', '', content_str_y.extract()[0])
        #     alna['title'] = title_str.extract()[0]
        #     alna['content'] = content
        #     alna['str_size'] = len(content)

        yield youm