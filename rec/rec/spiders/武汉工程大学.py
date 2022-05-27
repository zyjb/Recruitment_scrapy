# import re
# from urllib.parse import urljoin
#
# import scrapy
# from scrapy import Request
# from rec.items import RecItem, FailItem
# import json
# import requests
# from rec.base import Base
# import pandas as pd
# import numpy as np
#
#
# class WhgcSpider(scrapy.Spider):
#     name = 'whgc_university'
#     start_urls = ['http://jyb.wit.edu.cn/module/careers']
#     if name.endswith('large'):
#         custom_settings = {
#             'ITEM_PIPELINES': {'rec.pipelines.FailPipeline': 200, }
#         }
#     else:
#         custom_settings = {
#             'ITEM_PIPELINES': {'rec.pipelines.RecPipeline': 300, }
#         }
#
#     def __init__(self):
#         self.base = Base()
#
#     def parse(self, response):  # 获取宣讲会url
#         urls = [response.urljoin(i) for i in response.xpath('//a[@class="item-link"][@title]/@href').extract()]
#         title = [response.urljoin(i) for i in response.xpath('//a[@class="item-link"][@title]/@title').extract()]
#         for i in urls:
#             yield Request(i, callback=self.prase_detail, meta={
#                 'title': title,
#             }, dont_filter=True)
#
#     def prase_detail(self, response):
#         items = RecItem()
#         items['Seminar_title'] = response.meta.get('title')
#         items['Seminar_site'] = response.xpath(
#             '//div[@class="dm-cont"]/p[contains(.,"宣讲地点")]/text()').extract_first()  # 宣讲会地点
#         items['Seminar_college'] = '武汉工程大学'  # 宣讲会举办学校
#         items['Seminar_url'] = response.url
#         items['Seminar_time'] = response.xpath(
#             '//div[@class="dm-cont"]/p[contains(.,"宣讲时间")]/text()').extract_first()
#         yield items
