# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
from weibo.items import TextItem,WeiboCommentItem


class WeiboPipeline(object):
    def process_item(self, item, spider):
        return item

class MySQLPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        # 从项目的配置文件中读取相应的参数
        cls.MYSQL_DB_NAME = crawler.settings.get("MYSQL_DB_NAME", 'poas')
        cls.HOST = crawler.settings.get("MYSQL_HOST", 'localhost')
        cls.PORT = crawler.settings.get("MYSQL_PORT", 3306)
        cls.USER = crawler.settings.get("MYSQL_USER", 'root')
        cls.PASSWD = crawler.settings.get("MYSQL_PASSWORD", 'root')
        return cls()

    def open_spider(self, spider):
        self.dbpool = adbapi.ConnectionPool('pymysql', host=self.HOST, port=self.PORT, user=self.USER, passwd=self.PASSWD, db=self.MYSQL_DB_NAME, charset='utf8')

    def close_spider(self, spider):
        self.dbpool.close()

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.insert_db, item)

        return item

    def insert_db(self, tx, item):
        if isinstance(item,TextItem):
            values = (
                item['weibo_id'],
                item['user_id'],
                item['comments_count'],
                item['attitudes_count'],
                item['reposts_count'],
                item['text'],
                item['followers_count']
            )
            sql = 'INSERT INTO weibo_text(weibo_id,user_id,comments_count,attitudes_count,reposts_count,text,followers_count) VALUES (%s,%s,%s,%s,%s,%s,%s)'
            tx.execute(sql, values)
        else:
            values = (
                item['article_id'],
                item['comment_id'],
                item['user_id'],
                item['text'],
            )
            sql = 'INSERT INTO weibo_comment(article_id,comment_id,user_id,text) VALUES (%s,%s,%s,%s)'
            tx.execute(sql, values)

