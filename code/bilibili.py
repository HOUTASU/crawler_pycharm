#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @Author : sw
# @Time   : 2018/7/31 10:36
import requests
import json
import csv
from multiprocessing.dummy import Pool as ThreadPool
import time

# http://api.bilibili.com/x/web-interface/newlist?rid={rid}&pn={pn}&ps={ps}
comic_list = []
urls = []


def get_url():
    url = 'http://api.bilibili.com/x/web-interface/newlist?rid=32&pn='
    for i in range(1, 328):
        urls.append(url + str(i) + '&ps=50')


def get_message(url):
    print(url)
    time.sleep(1)
    try:
        r = requests.get(url, timeout=5)
        data = json.loads(r.text)['data']['archives']
        for j in range(len(data)):
            content = {}
            content['aid'] = data[j]['aid']
            content['title'] = data[j]['title']
            content['view'] = data[j]['stat']['view']
            content['danmaku'] = data[j]['stat']['danmaku']
            content['reply'] = data[j]['stat']['reply']
            content['favorite'] = data[j]['stat']['favorite']
            content['coin'] = data[j]['stat']['coin']
            comic_list.append(content)
    except Exception as e:
        print(e)


def write_to_file(comic_list):
    with open(r'..\result\bilibili-comic.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['aid', 'title', 'view', 'danmaku', 'reply', 'favorite', 'coin']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        try:
            writer.writerows(comic_list)
        except Exception as e:
            print(e)


get_url()
pool = ThreadPool(4)
pool.map(get_message, urls)
pool.close()
write_to_file(comic_list)
