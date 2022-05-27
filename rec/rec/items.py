# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RecItem(scrapy.Item):  # 宣讲会及小型招聘会(单个公司)
    Seminar_id = scrapy.Field()
    Seminar_time = scrapy.Field()  # 宣讲会时间段
    Seminar_site = scrapy.Field()  # 宣讲会地点
    Seminar_college = scrapy.Field()  # 宣讲会举办学校
    Seminar_partment = scrapy.Field()  # 宣讲会主办单位
    Seminar_url = scrapy.Field()
    Seminar_title = scrapy.Field()  # 标题


class FailItem(scrapy.Item):  # 大型招聘会
    Fail_title = scrapy.Field()  # 招聘会的题目
    Fail_time = scrapy.Field()  # 招聘会日期
    Fail_detail_time = scrapy.Field()  # 详细时间
    Fail_site = scrapy.Field()  # 宣讲会地点
    Fail_college = scrapy.Field()  # 招聘会举办学校
    Fail_url = scrapy.Field()
    Fail_partment = scrapy.Field()
