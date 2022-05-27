# coding=utf8
# -*- coding: utf-8 -*-
import os

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
# 导入time模块
import time
# 优化格式化化版本


os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'rec.settings')
process = CrawlerProcess(get_project_settings())
# 指定多个spider

# process.crawl("board_spider")
# process.crawl("favorite_spider")
# 执行所有 spider
with open('log.txt', 'a+') as f:
    times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    f.write(times+'启动了spiders')

for spider_name in process.spider_loader.list():
    # print spider_name
    process.crawl(spider_name)
    # print()
process.start()
