import os
import math
import json
import random
import requests
import datetime


# 获取天气和温度
def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['temp'])


# 每日一句
def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


# 字体随机颜色
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


def send_msg(token_dd, msg, at_all=False):
    """
    通过钉钉机器人发送内容
    @param date_str:
    @param msg:
    @param at_all:
    @return:
    """
    url = 'https://oapi.dingtalk.com/robot/send?access_token=' + token_dd
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    content_str = "早上好！\n\n{0}\n".format(msg)

    data = {
        "msgtype": "text",
        "text": {
            "content": content_str
        },
        "at": {
            "isAtAll": at_all
        },
    }
    res = requests.post(url, data=json.dumps(data), headers=headers)
    print(res.text)

    return res.text


if __name__ == '__main__':
    city = os.environ['CITY']
    token_dd = os.environ['TOKEN_DD']
    # city = "北京"
    # token_dd = '你自己的webhook后面的access_token复制在此'
    wea, temperature = get_weather()

    note_str = "当前城市：{0}\n今日天气：{1}\n当前温度：{2}\n{3}".format(city, wea, temperature, get_words())

    send_msg(token_dd, note_str, True)
