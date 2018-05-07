# -*- coding: utf-8 -*-
import scrapy
from myfirst.items import MyfirstItem


class SymptomspiderSpider(scrapy.Spider):
    name = 'symptomspider'
    allowed_domains = ['jbk.39.net']
    start_urls = ['http://jbk.39.net/bw_t2/']

    def parse(self, response):

        fu = response.xpath('//dt[@class="clearfix"]/h3/a/@title').extract()
        # fu = ['aaaa', 'bbbb']
        url_list = response.xpath('//dt[@class="clearfix"]/h3/a/@href').extract()
        # url_list= ['xxxx.com', 'xxxx.com']
        for i,j in zip(fu, url_list):
            item = MyfirstItem()
            item['name'] = i
            item['url'] = j
            yield item

        next_list = response.xpath('//div[@class="site-pages"]/a[@class="sp-a"]')

        for a in next_list:
            # print(a.xpath('./text()').extract_first())
            if a.xpath('./text()').extract_first() == '下页':
                next_url = 'http://jbk.39.net' + a.xpath('./@href').extract_first()
                print(next_url)
                yield scrapy.Request(url=next_url, callback=self.parse)
        # idtem['url'] = response.xpath('//dt[@class="clearfix"]/h3/a/@href')
        #pdrint(response.xpath('//dt[@class="clearfix"]/h3/a/@title').extract())

        # yield item
        # item['name']
        # item['url']