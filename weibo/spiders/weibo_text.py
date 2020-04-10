# -*- coding: utf-8 -*-
import scrapy
import json
import re
from weibo.items import TextItem
from urllib.parse import urlencode


class WeiboTextSpider(scrapy.Spider):
    name = 'm_weibo_spider'
    allowed_domains = ['m.weibo.cn/', 'weibo.com', 'weibo.cn']
    start_urls = ['https://passport.weibo.cn/signin/login']
    url = ""
    page = 0

    def __init__(self, keyword=None, *args, **kwargs):
        super(WeiboTextSpider, self).__init__(*args, **kwargs)
        print("==============", type(keyword))
        self.keywords = keyword

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
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103&%s&page_type=searchall'
        # 拼接第一条微博爬取链接
        key = {
            "type": 1
        }
        q = " "
        for i in self.keywords:
            q = q.join(str(i))
        key["q"] = q
        url = url % urlencode(key)
        self.url = url
        yield scrapy.Request(url, callback=self.crawl_data)

    def crawl_data(self, response):
        res = json.loads(response.text)
        items = res.get("data").get("cards")
        for item in items:
            if item.get("card_type") == 9:

                mblog = item.get("mblog")
                weibo_id = mblog.get("idstr")
                # 点赞
                attitudes_count = mblog["attitudes_count"]
                # 评论
                comments_count = mblog["comments_count"]
                # 转发
                reposts_count = mblog["reposts_count"]
                # 时间
                created_at = mblog["created_at"]
                user = mblog.get("user")
                user_id = user.get("id")
                followers_count = user["followers_count"]
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
                    print(result)
                text = TextItem()
                text["weibo_id"] = weibo_id
                text["user_id"] = user_id
                text["comments_count"] = comments_count
                text["attitudes_count"] = attitudes_count
                text["reposts_count"] = reposts_count
                text["created_at"] = created_at
                text["text"] = result
                text["followers_count"] = followers_count
                yield text

        while self.page < 100:
            self.page = self.page+1
            url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%E7%96%AB%E6%83%85' \
                  '&page_type=searchall'+"&page="+str(self.page)
            yield scrapy.Request(url, callback=self.crawl_data)


