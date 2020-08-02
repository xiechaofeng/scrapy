# -*- coding: utf-8 -*-
from urllib import request
import time
from datetime import datetime
import json
import requests

#获取数据
def get_data(url):
    headers = {
        'User_Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
    }
#    req = request.Request(url,headers = headers)
#    response = request.urlopen(req)
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.text
    return None

# 处理数据
def parse_data(html):
    data = json.loads(html)  # 将str转换为json
    comments = []
    for item in data['cmts']:
        comment = [
                str(item['approve']),
                item['cityName'] if 'cityName' in item else '',
                item['content'].replace('\n', '，').replace(',', '，'),
                str(item['id']),
                item['nick'],
                item['nickName'],
                str(item['reply']),
                str(item['score']),
                item['startTime'],
                str(item['userId']),
                str(item['userLevel'])
                ]
        comments.append(','.join(comment)+'\n')
    for item in data['hcmts']:
        comment = [
                str(item['approve']),
                item['cityName'] if 'cityName' in item else '',
                item['content'].replace('\n', '，').replace(',', '，'),
                str(item['id']),
                item['nick'],
                item['nickName'],
                str(item['reply']),
                str(item['score']),
                item['startTime'],
                str(item['userId']),
                str(item['userLevel'])
                ]
        comments.append(','.join(comment)+'\n')
    return comments

# 存储数据，存储到文本文件
def save_to_txt(movieid):
    # 获取当前时间，从当前时间向前获取
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#   millis = int(round(time.time() * 1000))
#    end_time = '2018-05-11 00:00:00'
    for i in range(50):
        url = 'http://m.maoyan.com/mmdb/comments/movie/{}.json?_v_=yes&offset='.format(str(movieid)) + str(15 * i) + '&startTime='+ start_time.replace(' ', '%20')
#       'https://m.maoyan.com/review/v2/comments.json?movieId=1211270&userId=-1&offset=' + str(15 * i) + '&limit=15&ts=1565881433629&type=3'
        try:
            html = get_data(url)
            print('success')
        except Exception as e:
            html = get_data(url)
        else:
            time.sleep(1)
        comments = parse_data(html)
#        start_time = comments[14]['startTime']  # 获得末尾评论的时间
#        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + timedelta(seconds=-1)  # 转换为datetime类型，减1秒，避免获取到重复数据
#        start_time = datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S')  # 转换为str
        with open('comments.txt', 'a',encoding='utf-8') as f:
            for comment in comments:
                f.write(comment)
save_to_txt(1211270)