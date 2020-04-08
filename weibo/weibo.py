import requests
import re
import json
import time

id_set = set()


def get_one_page(url):
    headers = {
        'Cookie': '_T_WM=87676225609; WEIBOCN_FROM=1110006030; '
                  'SUB=_2A25zgud9DeRhGeFK6lcS8S_MyjmIHXVQjIk1rDV6PUJbkdANLU3dkW1NQ5quImjPwJcMz46C7-6u6HsD8Rvaht6a; '
                  'SUHB=05i6fhEgA-LF5I; '
                  'SCF=Ar6EaJkdOpz6bwNNX-I0ADbCyYIvFztM3IRcJWPXt7Wi8n81YK0ZRwpFsPeCmeU0Io9HwFhUnRlUW7W7RZ9uKcU.; '
                  'SSOLoginState=1585878829; MLOGIN=1; M_WEIBOCN_PARAMS=lfid=102803&luicode=20000174&uicode=20000174; '
                  'XSRF-TOKEN=e0dd97'
        ,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'

    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return response.status_code


def main(i):
    if i == 0:
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type=1%26q%3D%E7%96%AB%E6%83%85&page_type' \
              '=searchall '
    else:
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type=1%26q%3D%E7%96%AB%E6%83%85&page_type' \
              '=searchall&page=' + str(i)
    html = get_one_page(url)
    print(html)
    if not isinstance(html, str):
        return
    res = json.loads(html)
    items = res.get("data").get("cards")
    for item in items:
        # print("!!!!!!!")
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
                # print(result)
            else:
                rough_results = mblog.get("text")
                # 去掉a标签和span标签
                result = re.sub('<.*?>|</.*?>|<s.*?>', '', rough_results)
                # "===============" +
                # print(weibo_id + " " + str(user_id) + " " + user_name + " " + result)
                # print(result)
            with open('weibo1.txt', 'a', encoding='utf-8') as file:

                file.write(result + '\n')
            # if comment_count > 0:
            #     comment_url = "https://m.weibo.cn/comments/hotflow?id=" + weibo_id + "&mid=" + weibo_id + "&max_id_type=0"
            #     max_id, max_id_type = get_comment(comment_url)
            #     if comment_count >= 20:
            #         while max_id != 0:
            #             url = "https://m.weibo.cn/comments/hotflow?id=" + weibo_id + "&mid=" + weibo_id + "&max_id=" + str(
            #                 max_id) + "&max_id_type=" + str(max_id_type)
            #             time.sleep(10)
            #             max_id, max_id_type = get_comment(url)
            #             print(max_id,max_id_type)


def get_comment(url):
    comment = get_one_page(url)

    # print("*****************下面是评论")
    if isinstance(comment, str):
        res = json.loads(comment)
        if res.get("data"):
            max_id = res.get("data").get("max_id")
            max_id_type = res.get("data").get("max_id_type")
            items = res.get("data").get("data")
            for item in items:
                rough_results = item.get("text")
                # 去掉a标签和span标签
                result = re.sub('<.*?>|</.*?>|<s.*?>', '', rough_results)
                with open('weibo.txt', 'a', encoding='utf-8') as file:
                    file.write(result + '\n')
                # print(result)
            # print("*****************上面是评论")
            return max_id, max_id_type

    return 0, 0


if __name__ == '__main__':
    i = 0
    while i < 100:
        main(i)
        i = i + 1
        time.sleep(10)
