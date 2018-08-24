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

from masrawy.items import  MasrawyItem

class masrawySpider(CrawlSpider):
    name = 'masrawy'
    allowed_domains = ['masrawy.com']

    categoryIds=[25,27,35,206,202,205,208,204,765,211,382,577,579,578,227,467,468,218,223,221,219,222,402,603,255,
                 235,254,582,583,122,375,378,379,376,598,61,50,51,56,445,446,215]
    allPage = 1600
    urls = []
    for   categoryId in   categoryIds:
        for page in range(1 ,1600,+1):
            url = 'http://www.masrawy.com/listing/SectionMore?categoryId='+str(categoryId)+'&pageIndex='+str(page)+'&hashTag=SectionMore'
            urls.append(url)

    start_urls = urls

    rules = (
        Rule(LinkExtractor(allow=('\.masrawy\.com\/.*',)), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=('\.news\/[0-9]+') ,restrict_xpaths=("//div[@class='post-cont']")),
        # callback="parse_item",follow=True),
        # Rule(LinkExtractor(allow=('\.news\/show\.aspx\?id=[0-9]+'),restrict_xpaths=("//div[@class='post-cont']")),
        # callback="parse_item",follow=True),
    )


    def parse_item(self, response):

        #print response.url

        masrawy = MasrawyItem()



        m2 = hashlib.md5()
        m2.update(response.url)

        masrawy['url'] = response.url
        masrawy['page_name'] = m2.hexdigest()
        masrawy['do_main'] = 'masrawy.com'

        title_str = response.xpath('//title/text()')
        content_str = response.xpath("//div[@class='content']//div[@class='details']//p/text()")
        # type_str = response.xpath('//div[@id="PressH"]/b') #分类

        if content_str and title_str:
            content = ""
            for s in content_str.extract():
                content += s

            masrawy['title'] = title_str.extract()[0]
            masrawy['content'] = content
            masrawy['str_size'] = len(content)

        # 分享页
        # content_str_y = response.xpath('//div[@id="content"]/div[@id="TPKcnt"]/p')
        # if content_str_y and title_str:
        #     content = re.sub(r'</?\w+[^>]*>', '', content_str_y.extract()[0])
        #     alna['title'] = title_str.extract()[0]
        #     alna['content'] = content
        #     alna['str_size'] = len(content)

        yield masrawy