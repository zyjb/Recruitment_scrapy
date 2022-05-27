import re
from urllib.parse import urljoin

import scrapy
from scrapy import Request
from ..items import RecItem
import json
import requests
from ..base import Base
import pandas as pd
import numpy as np


class WhRecSpider(scrapy.Spider):
    name = 'wuhan_university'
    start_urls = ['http://www.xsjy.whu.edu.cn/default.html']
    custom_settings = {
        'ITEM_PIPELINES': {'rec.pipelines.RecPipeline': 300, }
    }
    def __init__(self):
        self.base = Base()

    def parse(self, response):  # 获取宣讲会url
        # Seminar_url = response.xpath("//a[contains(text(),'专场招聘')]/@href").extract_first()
        data = {
            'queryModel.showCount': 100,
        }
        r = requests.post(url='http://www.xsjy.whu.edu.cn/zftal-'
                              'web/zfjy!wzxx!whdx10486/xjhxx_cxXjhForWeb.htm'
                              'l?doType=query', data=data)
        rr = json.loads(r.content)
        content = rr['items']
        for i in range(len(content)):
            temp = content[i]['sqbh']
            Seminar_content_url = 'http://www.xsjy.whu.edu.cn/zftal-web/zfjy!wzxx/zfjy!wzxx!whdx10486/xjhxx_ckXjhxx.html?sqbh=' + temp
            yield Request(response.urljoin(Seminar_content_url),
                          meta={
                              'Seminar_partment': content[i].get('xjhmc')
                          }, callback=self.prase_content, dont_filter=True)

    def prase_content(self, response):
        Seminar_time_date = self.base.wash(response.xpath("//span[conta"
                                                          "ins(text(),'日期')]/../text()").extract())
        items = RecItem()
        Seminar_site = self.base.wash(response.xpath("//span[contains(text(),'场地')]/../text()").extract())

        time1 = self.base.wash(response.xpath("//span[contains(text(),"
                                                     "'时间段')]/../text()").extract())
        time2 = Seminar_time_date
        time3 = self.base.wash(response.xpath('//span[contains(text(),"起止时间")]/../text()').extract())
        # Seminar_text = response.xpath("//div[@class='wordwrap']").extract_first()
        items['Seminar_college'] = '武汉大学'
        items['Seminar_title'] = response.xpath('//span[@class="ico"]/text()').extract_first()
        items['Seminar_url'] = response.url
        items['Seminar_partment'] = response.meta.get('Seminar_partment')
        items['Seminar_site'] = Seminar_site
        items['Seminar_time'] = self.base.date_merge(time2,time1,time3)
        # items['Seminar_text'] = Seminar_text
        yield items
