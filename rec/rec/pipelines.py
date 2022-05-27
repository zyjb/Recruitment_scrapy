# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .items import RecItem, FailItem
from .connect import Connection


class RecPipeline(object):
    def __init__(self):
        self.C = Connection()
        self.conn = self.C.get_conn()
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item, RecItem):
            select_to = '''select Seminar_id  from model_seminar where Seminar_url="{}"'''
            try:
                result = self.cursor.execute(select_to.format(item.get('Seminar_url')))

            except:
                print('错误代码：1001')
            if result == 0:
                info = ['Seminar_time', 'Seminar_site', 'Seminar_college', 'Seminar_partment',
                        'Seminar_url', 'Seminar_title']
                for i in info:
                    try:
                        item[i]
                    except:
                        item[i] = 'None'
                insert_to = 'insert into model_seminar(Seminar_time,Seminar_site,Seminar_' \
                            'college,Seminar_partment,Seminar_title,Seminar_url) VALUES ("{}","{}","{}","{}",' \
                            '"{}","{}")'
                try:
                    self.cursor.execute(insert_to.format(item['Seminar_time'],
                                                         item['Seminar_site'],
                                                         item['Seminar_college'], item['Seminar_partment']
                                                         , item['Seminar_title'], item['Seminar_url']))
                    self.conn.commit()
                except:
                    print('错误代码：1002')
                return item

    def closedb(self):
        self.conn.close()


class FailPipeline(object):
    def __init__(self):
        self.C = Connection()
        self.conn = self.C.get_conn()
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item, FailItem):
            select_to = '''select Fail_id  from model_fail where Fail_url="{}"'''
            try:
                result = self.cursor.execute(select_to.format(item.get('Fail_url')))
            except:
                print('错误代码：1001')
            if result == 0:
                info = ['Fail_title', 'Fail_time', 'Fail_college', 'Fail_site', 'Fail_partment', 'Fail_url',
                        'Fail_detail_time']
                for i in info:
                    try:
                        item[i]
                    except:
                        item[i] = 'None'

                insert_to = 'insert into model_fail(Fail_title,Fail_college, Fail_time, Fail_detail_time, Fail_site, ' \
                            'Fail_url,Fail_partment) VALUES ("{}","{}","{}",' \
                            '"{}","{}","{}","{}")'
                try:
                    self.cursor.execute(insert_to.format(item['Fail_title'], item['Fail_college'], item['Fail_time'],
                                                         item['Fail_detail_time'], item['Fail_site'],
                                                         item['Fail_url'], item['Fail_partment']
                                                         ))
                    self.conn.commit()
                except:
                    print('错误代码：1002')
                return item

    def closedb(self):
        self.conn.close()
