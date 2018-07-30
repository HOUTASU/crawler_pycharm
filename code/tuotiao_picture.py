#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @Author : sw
# @Time   : 2018/7/30 18:49

import requests
import json
import re


# https://www.toutiao.com/search_content/?
# offset=20&format=json&keyword=bilibili&autoload=true&count=20&cur_tab=3&from=gallery
def get_page_list():
    json_url = 'https://www.toutiao.com/search_content?'
    group_id = []
    for i in range(3):
        full_json_url = json_url + 'offset=' + str(
            i * 20) + '&format=json&keyword=bilibili&autoload=true&count=20&cur_tab=3&from=gallery'
        r = requests.get(full_json_url)
        json_content = json.loads(r.text)
        for i in json_content['data']:
            group_id.append(i['id'])
    return group_id


def get_one_page(group_id, pic_list):
    url = 'https://www.toutiao.com/a'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    for i in group_id:
        picture_url = url + str(i)
        r = requests.get(picture_url, headers=headers)
        pre = re.compile(r'pb9.pstatp.com\\\\/origin\\\\/[\w]+')
        p_list = pre.findall(r.text)
        print(len(p_list))
        for j in range(len(p_list)):
            p_list[j] = 'http://' + p_list[j].replace('\\', '')
            print(p_list[j])
            try:
                rp = requests.get(p_list[j], headers=headers, timeout=5)
                if rp.status_code == 200:
                    pic_list.append(rp.content)
            except:
                pass


group_id = get_page_list()
pic_list = []
get_one_page(group_id, pic_list)
file_dir = r'D:\toutiao-picture\\'
for index, pic in enumerate(pic_list):
    with open(file_dir + str(index) + '.jpg', 'wb') as f:
        f.write(pic)
