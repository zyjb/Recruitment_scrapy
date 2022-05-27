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


class ZnRecSpider(scrapy.Spider):
    name = 'znmz_university'
    start_urls = ['http://job.scuec.edu.cn/eweb/jygl/zpfw.so?modcode=jygl_xjhxxck&subsyscode=zpfw&type=searchXjhxx'
                  '&xjhType=all']
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
        items = RecItem()
        items['Seminar_title'] = response.xpath('//div[@class="z_newsl"]/ul/li[2]/div[2]/text()').extract_first()
        items['Seminar_college'] = '中南名族大学'
        items['Seminar_site'] = response.xpath('//div[@class="z_newsl"]/ul/li[2]/div[3]/text()').extract_first()
        items['Seminar_partment'] = response.xpath('//div[@class="z_newsl"]/ul/li[2]/div[1]/a/text()').extract_first()
        time1 = response.xpath('//div[@class="z_newsl"]/ul/li[2]/div[4]/text()').extract_first()
        time2 = response.xpath('//div[@class="z_newsl"]/ul/li[2]/div[5]/text()').extract_first()
        items['Seminar_time'] = self.base.date_merge(time1, ' ', time2)
        onclick = (response.xpath('//div/a/@onclick[contains(.,"view")]').extract_first()).replace('viewXphxx', '')
        url_ = 'http://job.scuec.edu.cn/eweb/jygl/zpfw.so?modcode=jygl_xjhxxck&subsyscode=zpfw&type=viewXjhxx&id='
        items['Seminar_url'] = url_ + self.base.cull(onclick)
        yield items
        # url = url + '/index?page='
        # for i in range(1, 5, 1):
        #     url_ = url + str(i)
        #     yield Request(url_, callback=self.prase_content, dont_filter=True)
