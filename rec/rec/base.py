import time
import re

class Base(object):
    def __init__(self):
        pass

    def is_ustr(self, in_str):
        """清洗获取到的数据,只留下汉字"""
        out_str = ''
        for i in in_str:
            if self.is_uchar(i):
                out_str = out_str + i
        return out_str

    def is_uchar(self, uchar):
        """判断一个unicode是否是汉字"""
        if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
            return True
        return False

    def wash(self, l):
        """如果拿到多条或一条数据,且一定有一条数据非空,则使用此方法"""
        return ''.join([i.strip() for i in l])

    def date_merge(self, date1, date2, date3):  # 由年份+月份+上下午+时间
        return date1 + ' ' + date2 + ' ' + date3

    def merge(self, detail):
        # 将多个xml对象合并为字符串
        text = ''
        for i in detail:
            i = ''.join(i.split())
            text = text + i if len(i) == 0 else text + i + ','
        return text

    def cull(self, s):
        # 替换掉爬取到数据中的冗余信息
        return s.replace('(', '').replace(')', '').replace('\'', '').replace('\\', '')
