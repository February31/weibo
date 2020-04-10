# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# 微博文章自定义对象
class TextItem(scrapy.Item):
    # 微博id
    weibo_id = scrapy.Field()
    # 用户id
    user_id = scrapy.Field()
    # 点赞
    attitudes_count = scrapy.Field()
    # 时间
    created_at = scrapy.Field()
    # 评论数
    comments_count = scrapy.Field()
    # 转发
    reposts_count = scrapy.Field()
    # 微博内容
    text = scrapy.Field()
    # 博主粉丝数
    followers_count = scrapy.Field()


# 评价内容自定义对象
class WeiboCommentItem(scrapy.Item):
    article_id = scrapy.Field()  # 微博id
    comment_id = scrapy.Field()  # 评价id
    user_id = scrapy.Field()  # 评价人编号
    text = scrapy.Field()  # 评价内容
    # created_at = scrapy.Field()  # 创建时间


# # 评价url
# class CommentUrlItem(scrapy.Item):
#     url = scrapy.Field()
#     weibo_id = scrapy.Field()

# # 微博用户自定义对象
# class WeiBoUserItem(scrapy.Item):
#     sentiment_id = scrapy.Field()  # 舆情ID
#     description = scrapy.Field()  # 描述
#     id = scrapy.Field()  # 用户id
#     screen_name = scrapy.Field()  # 用户名
#     follow_count = scrapy.Field()  # 关注度
#     followers_count = scrapy.Field()  # 粉丝数
#     url = scrapy.Field()  # 用户访问地址
#     gender = scrapy.Field()  # 性别