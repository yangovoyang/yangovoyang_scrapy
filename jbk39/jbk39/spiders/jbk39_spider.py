# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
import os

class Jbk39SpiderSpider(scrapy.Spider):
    name = 'jbk39_spider'
    allowed_domains = ['jbk.39.net']
    start_urls = ['http://jbk.39.net/bw/xinzang_t1']

    def __init__(self):
        if os._exists('log.txt'):
            os.remove('log.txt')
        if os._exists('result.json'):
            os.remove('result.json')

    def parse(self, response):
        disease_list = response.xpath("//div[@id='res_tab_2']/div[@class='res_list']/dl[1]/dt[1]/h3[1]/a[1]/@href").extract()
        for item in disease_list:
            yield scrapy.Request(url=item, callback=self.extract_basic)

        # next page
        pages = response.xpath("//div[@class='site-pages']/a[@class='sp-a']")
        for page in pages:
            # print(page.xpath("text()").extract_first())
            if page.xpath("text()").extract()[0] == '下页':
                # print('http://jbk.39.net' + page.xpath("@href").extract_first())
                yield scrapy.Request(url='http://jbk.39.net' + page.xpath("@href").extract_first(), callback=self.parse)

    def extract_basic(self, response):
        """extract basic information of the disease"""
        name = response.xpath("//div[@class='spreadhead']/div[2]/a[1]/h1[1]/text()").extract_first()
        # alias = response.xpath("//div[@class='spreadhead']/div[2]/h2/text()").extract_first()
        li_list = response.xpath("//div[@class='info']/ul[1]/li")
        dict = {}
        for li in li_list:
            dict['name'] = name
            str = li.extract()
            # print(str)
            # filter
            if 'cite' not in str:
                extract_list = re.findall('>\\s?([^><\\n]+)<', str)
                # print(name, extract_list)
                if len(extract_list) < 2:
                    with open('log.txt', 'a', encoding='utf8') as file:
                        file.write(time.strftime('%Y-%m-%d %H:%M:%S') + ': ' + name + '的' + extract_list[0] + '抽取失败！ ' + response.url + '\n')
                else:
                    key = extract_list[0][:-1]
                    value = extract_list[1]
                    dict[key]=value
        if len(dict) == 0:
            with open('log.txt', 'a', encoding='utf8') as file:
                file.write(time.strftime('%Y-%m-%d %H:%M:%S') + ': ' + name + '的基本信息爬取失败，请手动抽取！ ' + response.url + '\n')
        else:
            with open('result.json', 'a', encoding='utf8') as file:
                dict['url'] = [response.url]
                file.write(json.dumps(dict, ensure_ascii=False)+'\n')

    # def extract_symptom(self):
