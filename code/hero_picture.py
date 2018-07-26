#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @Author : sw
# @Time   : 2018/7/26 18:56
import requests
import os
import json


def get_hero_list():
    with open(r'..\resource\herolist.json', 'rb') as f:
        hero_list = json.loads(f.read())
    return hero_list
    pass


def get_hero_picture(pic_url):
    try:
        r = requests.get(pic_url)
        return r.content
    except Exception as e:
        print('获取图片失败')
        print(e)


def main():
    hero_list = get_hero_list()
    url = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/'
    file_dir = r'D:\hero-picture\\'

    for i in hero_list:
        for j in range(len(i['skin_name'].split('|'))):
            pic_url = url + str(i['ename']) + '/' + str(i['ename']) + '-bigskin-' + str(j + 1) + '.jpg'
            picture = get_hero_picture(pic_url)
            with open(file_dir + i['skin_name'].split('|')[j] + '.jpg', 'wb') as f:
                f.write(picture)
        print("%s, %s" % (i['ename'], i['cname']))


if __name__ == '__main__':
    main()
