import re
from urllib.parse import urljoin

import scrapy
from scrapy import Request
from ..items import FailItem
import json
import requests
from ..base import Base
from urllib.parse import urljoin


class WhSeminarItemSpider(scrapy.Spider):
    name = 'wuhan_university_large'
    start_urls = ['http://www.xsjy.whu.edu.cn/default.html']
    custom_settings = {
        'ITEM_PIPELINES': {'rec.pipelines.FailPipeline': 200, }
    }

    def __init__(self):
        self.base = Base()

    def parse(self, response):  # 获取宣讲会url
        url = 'http://www.xsjy.whu.edu.cn/zftal-web/zfjy!wzxx!whdx10486/zphxx_cxWzZphxxNry.html?doType=query'
        data = {
            'queryModel.showCount': '100',
        }
        r = requests.post(url=url, data=data)
        rr = json.loads(r.content)  #转化成json数据结构
        content = rr.get('items')
        for i in range(len(content)):
            _url = 'http://www.xsjy.whu.edu.cn/zftal-web/zfjy!wzxx!whdx10486/zphxx_ckWzZphxx.html?zphbh' \
                   '='
            parse_url = _url + content[i].get('zphbh')
            site = content[i].get('cdmc')
            large_time = content[i].get('zphrq')
            yield Request(parse_url, callback=self.prase_content,
                          meta={
                              'time': large_time,
                              'site': site,
                          }, dont_filter=True)#去重

    def prase_content(self, response):
        item = FailItem()
        Fail_title = response.xpath('//div[@class="position_infor"]/h3/span/text()').extract_first()
        Fail_time = ''.join(response.xpath('//div[@class="con"]/p[2]/text()').extract())  # 招聘会时间
        Fail_detail_time = response.meta.get('time')
        Fail_site = response.meta.get('site')  # 宣讲会地点
        Fail_url = response.url
        item['Fail_title'] = Fail_title  # 招聘会的标题
        item['Fail_time'] = Fail_time  # 招聘会日期
        item['Fail_detail_time'] = Fail_detail_time  # 详细时间
        item['Fail_site'] = Fail_site  # 宣讲会地点
        item['Fail_url'] = Fail_url
        item['Fail_college'] = '武汉大学'
        yield item
