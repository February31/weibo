# -*- coding: utf-8 -*-
import scrapy
import json
import re


class MWeiboSpiderSpider(scrapy.Spider):
    name = 'm_weibo_spider'
    allowed_domains = ['m.weibo.cn/', 'weibo.com', 'weibo.cn']
    start_urls = ['https://passport.weibo.cn/signin/login']

    def parse(self, response):
        url = "https://passport.weibo.cn/sso/login"
        formdata = {
            "username": "17780546500",
            "password": "pythonspider",
            "savestate": "1",
            "ec": "0",
            "r": "https://m.weibo.cn/",
            "pagerefer": "https://m.weibo.cn/login?backURL=https%253A%252F%252Fm.weibo.cn%252F",
            "entry": "mweibo",
            "mainpageflag": "1"
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/77.0.3865.120 Safari/537.36'
        }
        yield scrapy.FormRequest(url, formdata=formdata, headers=headers, callback=self.login_success)

    def login_success(self, response):
        print("=" * 20)
        # &page=3
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%E7%96%AB%E6%83%85' \
              '&page_type=searchall '
        yield scrapy.Request(url, callback=self.crawl_data)

    def crawl_data(self, response):
        res = json.loads(response.text)
        items = res.get("data").get("cards")
        for item in items:
            print("!!!!!!!")
            if item.get("card_type") == 9:

                mblog = item.get("mblog")
                weibo_id = mblog.get("idstr")
                comment_count = mblog.get("comments_count")
                # user = mblog.get("user")
                # user_id = user.get("id")
                # user_name = user.get("screen_name")
                # if weibo_id not in id_set:
                #     id_set.add(weibo_id)
                if mblog.get("longText"):
                    rough_results = mblog.get("longText")["longTextContent"]
                    # 去掉网址
                    result = re.sub('[a-zA-z]+://[^\s]*', '', rough_results)
                    # print(weibo_id + " " + str(user_id) + " " + user_name + " " + result)
                    print(result)
                else:
                    rough_results = mblog.get("text")
                    # 去掉a标签和span标签
                    result = re.sub('<.*?>|</.*?>|<s.*?>', '', rough_results)
                    # "===============" +
                    # print(weibo_id + " " + str(user_id) + " " + user_name + " " + result)
                    print(result)
                # if comment_count > 0:
                #     url = "https://m.weibo.cn/comments/hotflow?id=" + weibo_id + "&mid=" + weibo_id + "&max_id_type=0"
                #     scrapy.Request(url, callback=self.crawl_comment)
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%E7%96%AB%E6%83%85' \
              '&page_type=searchall'
        yield scrapy.Request(url, callback=self.crawl_data)


    def crawl_comment(self, response):
        print("*****************下面是评论")
        res = json.loads(response.text)
        max_id = res.get("data").get("max_id")
        max_id_type = res.get("data").get("max_id")
        items = res.get("data").get("data")
        for item in items:
            rough_results = item.get("text")
            # 去掉a标签和span标签
            result = re.sub('<.*?>|</.*?>|<s.*?>', '', rough_results)
            print(result)
        print("*****************上面是评论")
        # if max_id>0:
        #     url = ""
        #     yield
