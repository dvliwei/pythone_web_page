# -*- coding: utf-8 -*-

import scrapy
import re
from scrapy.spider import Request
import  hashlib

#crawlspider,rule配合使用可以起到遍历全站的作用，request为请求的接口

from scrapy.spider import CrawlSpider,Rule
#配合使用Rule进行url规则匹配
from scrapy.linkextractors import LinkExtractor

from myoum7.items import  Myoum7Item

class youmSpider(CrawlSpider):
    name = 'myoum7'
    allowed_domains = ['m.youm7.com']


    categoryIds=[65,319,97,203,12,298,341,332,88,297,286,192,48,251,94,89,245,291,328,296,335]
    #categoryIds = [65]
    urls = []
    for   categoryId in   categoryIds:
        url = 'https://m.youm7.com/Section/NewsSectionPaging?lastid=9/10/2018 11:43:13 PM&sectionID=' + str(categoryId)
        urls.append(url)

    start_urls = urls

    rules = (
        Rule(LinkExtractor(allow=('m\.youm7\.com\/.*',)), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=('\.news\/[0-9]+') ,restrict_xpaths=("//div[@class='post-cont']")),
        # callback="parse_item",follow=True),
        # Rule(LinkExtractor(allow=('\.news\/show\.aspx\?id=[0-9]+'),restrict_xpaths=("//div[@class='post-cont']")),
        # callback="parse_item",follow=True),
    )


    def parse_item(self, response):

        m2 = hashlib.md5()
        m2.update(response.url)

        youm = Myoum7Item()
        youm['url'] = response.url
        youm['page_name'] = m2.hexdigest()
        youm['do_main'] = 'm.youm7.com'


        referer = response.request.headers.get('Referer', None)

        reattr = re.findall(r"sectionID=(\w+)", referer)
        if reattr:
            youm['url'] = referer
            yield Request(referer, callback=self.parse_item)

        date_str = response.xpath('//div[@class="news-dev"]/@data-id')

        attr = re.findall(r"sectionID=(\w+)", response.url)

        if date_str and attr:
            sectionID = attr[0]
            date_str = date_str.extract()
            url_date = date_str[len(date_str)-1]
            newUrl = "https://m.youm7.com/Section/NewsSectionPaging?lastid="+url_date+"&sectionID="+str(sectionID)
            youm['url'] = newUrl
            yield Request(newUrl, callback=self.parse_item)

        title_str = response.xpath('//title/text()')

        content_str = response.xpath('//div[@class="text-cont"]//div[@id="articleBody"]//p/text()')

        type_str =response.xpath('//div[@class="container"]//div[@class="breadcumb"]//a/text()')#菜单中的分类

        if content_str and title_str:
            content = ""
            content_str =  response.xpath('//div[@class="text-cont"]//div[@id="articleBody"]//p/text()')
            for s in content_str.extract():
                content += s

            youm['title'] = title_str.extract()[0]
            youm['content'] = content
            youm['str_size'] = len(content)
            youm['type'] = type_str.extract()[1] #取详细页中的分类



        yield youm




