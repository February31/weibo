# -*- coding: utf-8 -*-
import scrapy
import json
from pyquery import PyQuery


class WeiboSpiderSpider(scrapy.Spider):
    name = 'weibo_spider'
    allowed_domains = ['weibo.com','weibo.cn']
    start_urls = ['https://passport.weibo.cn/signin/login']


    def parse(self, response):
        print(response.text)
        print("-"*20)
        url = "https://passport.weibo.cn/sso/login"
        formdata = {
            "username":"17780546500",
            "password":"pythonspider",
            "savestate":"1",
            "ec":"0",
            "r":"https://m.weibo.cn/",
            "pagerefer":"https://m.weibo.cn/login?backURL=https%253A%252F%252Fm.weibo.cn%252F",
            "entry":"mweibo",
            "mainpageflag":"1"
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/77.0.3865.120 Safari/537.36'
        }
        yield scrapy.FormRequest(url,formdata=formdata,headers=headers,callback=self.login_success)

    def login_success(self,response):
        print("="*20)
        res = json.loads(response.text)
        login_success_url=res["data"]["crossdomainlist"]["weibo.com"]
        yield scrapy.Request(url=login_success_url,callback=self.crawl_data)

    def crawl_data(self,response):
        print("+"*20)
        yield scrapy.Request(url="https://weibo.com", callback=self.login_success_after)

    def login_success_after(self,response):
        # cookie = response.headers.getlist("Set-Cookie")
        # print("生成的cookies:",cookie)
        # print(response.text)
        return scrapy.Request(url="https://s.weibo.com/weibo?q=疫情&typeall=1&suball=1&timescope=custom:2020-03-20-10:2020-03-21-13&Refer=g",callback=self.crawl_weibo)

    def crawl_weibo(self,response):
        # card_wraps = response.xpath('//*[@id="pl_feedlist_index"]/div[2]//div[@class="card-wrap"]')
        # # print(card_wraps)
        # # print(type(card_wraps))
        # # for card_wrap in card_wraps:
        # #     text = card_wrap.xpath('//div/div[1]/div[2]/p[1]')
        # #     print(text)
        # #     print(type(text))
        # print(len(card_wraps))
        # text = card_wraps[0].xpath('//div/div[1]/div[2]/p[1]/text()')
        # print(text)
        # print(type(text))
        doc = PyQuery(response.text)
        contents = doc('.card-wrap .content > p.txt').items()
        for content in contents:
            print(content.text())

#     1。选择时间，然后利用高级搜索一页一页的爬取。
# 2. 不仅要爬取内容，还要爬取评论，也就是还要深入进去，然后把所有的评论都爬取下来。
# 1.首先要做的是先爬第一页的第一条，然后尽量把需要的数据都爬取到。

