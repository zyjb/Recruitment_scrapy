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


class DdlSpider(scrapy.Spider):
    name = 'dd_university_large'
    start_urls = ['https://www.baidu.com/']
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
        url = 'https://cug.91wllm.com/jobfair/index?page={}'
        for i in range(1, 5, 1):  # 翻页限制
            url_ = url.format(str(i))
            yield Request(url_, callback=self.prase_content, dont_filter=True)

    def prase_content(self, response):
        urls = [response.urljoin(i) for i in response.xpath('//div[@id="mCon"]/ul/li/a/@href').extract()]
        for i in urls:
            yield Request(i, callback=self.prase_detail, dont_filter=True)

    def prase_detail(self, response):
        items = FailItem()
        items['Fail_title'] = response.xpath('//div[@class="viewHead"]/h1/text()').extract_first()
        items['Fail_time'] = self.base.wash(response.xpath(
            '//ul[@class="xInfo xInfo-2 cl tInfo-2"]/li[contains(text(),"具体时间")]/span/text()').extract())
        items['Fail_site'] = response.xpath(
            '//ul[@class="xInfo xInfo-2 cl tInfo-2"]/li[contains(text(),"举办地址")]/span/text()').extract_first()
        if items['Fail_site']:
            pass
        else:
            items['Fail_site'] = response.xpath(
                '//ul[@class="xInfo xInfo-2 cl tInfo-2"]/li[contains(text(),"宣讲类别")]/span/text()').extract_first()
        items['Fail_url'] = response.url
        items['Fail_college'] = '中国地质大学'
        yield items
