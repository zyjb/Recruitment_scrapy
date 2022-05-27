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


class QglRecSpider(scrapy.Spider):
    name = 'wuqg_university_large'
    start_urls = ['https://whpu.91wllm.com/jobfair']
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
        urls = [response.urljoin(i) for i in response.xpath('//div[@id="mCon"]/ul/li/a/@href').extract()]
        for i in urls:
            yield Request(i, callback=self.prase_detail, dont_filter=True)

    def prase_detail(self, response):
        items = FailItem()
        items['Fail_title'] = response.xpath('//div[@class="viewHead"]/h1/text()').extract_first()  # 宣讲会时间段
        items['Fail_site'] = response.xpath(
            '//ul[@class="xInfo xInfo-2 cl tInfo-2"]/li[contains(text(),"举办地址")]/span/text()').extract_first()  # 宣讲会地点
        if items['Fail_site']:
            pass
        else:
            items['Fail_site'] = response.xpath(
                '//ul[@class="xInfo xInfo-2 cl tInfo-2"]/li[contains(text(),"宣讲类别")]/span/text()').extract_first()
        items['Fail_college'] = '武汉轻工大学'  # 宣讲会举办学校
        items['Fail_url'] = response.url
        items['Fail_time'] = response.xpath(
            '//ul[@class="xInfo xInfo-2 cl tInfo-2"]/li[contains(text(),"具体时间")]/span/text()').extract_first()
        yield items
