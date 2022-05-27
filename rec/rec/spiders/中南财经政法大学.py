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


class ZnlSpider(scrapy.Spider):
    name = 'zncj_university'
    start_urls = ['http://jyzx.zuel.edu.cn/career/preachmore']
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
        urls = response.xpath("//table[@id='h26']/tbody/tr/td/a/@href").extract()
        for i in urls:
            yield Request(response.urljoin(i), callback=self.prase_content, dont_filter=True)

    def prase_content(self, response):
        Items = RecItem()
        items = RecItem()
        items['Seminar_title'] = self.base.wash(response.xpath('//div[@class="dm-title"]/text()').extract_first())  # 宣讲会时间段)
        items['Seminar_site'] = response.xpath(
            '//th[contains(.,"地点")]/../td/text()').extract_first()  # 宣讲会地点
        items['Seminar_college'] = '中南财经政法大学'  # 宣讲会举办学校
        items['Seminar_url'] = response.url
        items['Seminar_time'] = self.base.wash(response.xpath(
            '//th[contains(.,"举办时间")]/../td/text()').extract_first())
        yield items
