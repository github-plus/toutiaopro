# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymysql

class ToutiaoproPipeline:
    def process_item(self, item, spider):
        tiele = item['title']
        #print(tiele)
        return item

class mysqlPipeLine(object):
    conn = None
    cursor = None
    def open_spider(self,spider):
        self.conn = pymysql.Connect(host='MYSQL地址',port=3306,user='账号',password='密码',db='python',charset='utf8')
    def process_item(self,item,spider):
        self.cursor = self.conn.cursor()
        try:
            tiele = item['title']
            print(tiele)
            self.cursor.execute('insert into toutiao (title,content,time,author) values("%s","%s","%s","%s")'%(item["title"],item["content"],item["time"],item["author"]))
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        return item
    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()