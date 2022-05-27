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


class ZnlRecSpider(scrapy.Spider):
    name = 'znmz_university_large'
    start_urls = ['http://job.scuec.edu.cn/eweb/jygl/zpfw.so?type=zph']
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
        onclicks = response.xpath('//div[@class="d_lb"]/div//ul/li[1]/a/@onclick').extract()
        for i in onclicks:
            onclick = self.base.cull(i.replace('viewZphxx', ''))
            url_ = 'http://job.scuec.edu.cn/eweb/jygl/zpfw.so?modcode=jygl_zphxxck&subsyscode=zpfw&type=viewZphxx&id='+onclick
            yield Request(url_, callback=self.prase_content, dont_filter=True)

    def prase_content(self, response):
        items = FailItem()
        items['Fail_title'] = response.xpath('//td[contains(text(),"主题")]/following-sibling::td/text()').extract_first()
        items['Fail_time'] = response.xpath('//td[contains(text(),"举办日期")]/following-sibling::td/text()').extract_first()
        items['Fail_site'] = response.xpath('//td[contains(text(),"举办地点")]/following-sibling::td/text()').extract_first()
        items['Fail_url'] = response.url
        items['Fail_college'] = '中南名族大学'
        yield items

