import re
from urllib.parse import urljoin

import scrapy
from scrapy import Request
from rec.items import RecItem, FailItem
import json
import requests
from rec.base import Base
import pandas as pd
import numpy as np


class HnlSpider(scrapy.Spider):
    name = 'hzny_university'
    start_urls = ['https://hzau.91wllm.com/']
    if name.endswith('large'):
        custom_settings = {
            'ITEM_PIPELINES': {'rec.pipelines.FailPipeline': 200, }
        }
    else:
        custom_settings = {
            'ITEM_PIPELINES': {'rec.pipelines.RecPipeline': 300, }
        }

    def __init__(self):
        self.base = Base()

    def parse(self, response):  # 获取宣讲会url
        url = response.xpath("//a[contains(text(),'线上宣讲')]/@href").extract_first()
        if url:
            pass
        else:
            url = response.xpath("//a[contains(text(),'校内宣讲')]/@href").extract_first()
        url = url + '/index?page='
        for i in range(1, 5, 1):
            url_ = url + str(i)
            yield Request(url_, callback=self.prase_content, dont_filter=True)

    def prase_content(self, response):
        urls = [response.urljoin(i) for i in response.xpath('//div[@class="infoBox mt10"]/ul/li/a/@href').extract()]
        for i in urls:
            yield Request(i, callback=self.prase_detail, dont_filter=True)

    def prase_detail(self, response):
        items = RecItem()
        items['Seminar_title'] = response.xpath('//div[@class="viewHead"]/h1/text()').extract_first()  # 宣讲会时间段
        items['Seminar_site'] = response.xpath(
            '//ul[@class="xInfo xInfo-2 cl tInfo-2"]/li[contains(text(),"宣讲地址")]/span/text()').extract_first()  # 宣讲会地点
        items['Seminar_college'] = '华中农业大学'  # 宣讲会举办学校
        items['Seminar_url'] = response.url
        items['Seminar_time'] = response.xpath(
            '//ul[@class="xInfo xInfo-2 cl tInfo-2"]/li[contains(text(),"宣讲时间")]/span/text()').extract_first()
        yield items
