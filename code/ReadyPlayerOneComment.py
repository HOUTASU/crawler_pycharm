import requests
from bs4 import BeautifulSoup
import csv
import time


def get_one_page(url, result):
    try:
        headers = 'User-Agent:Mozilla/5.0 (Windows; U;' \
                  ' Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) ' \
                  'Version/5.1 Safari/534.50'
        r = requests.get(url, headers)
        r.encoding = 'utf-8'
        html = r.text
        parser_one_page(html, result)
    except:
        return


def parser_one_page(html, result):
    soup = BeautifulSoup(html, 'html.parser')
    comments = soup.select('.comment-item')
    for index in range(len(comments)):
        com = {}
        com['user'] = comments[index].select('.comment-info a')[0].text.strip()
        com['time'] = comments[index].select('.comment-time')[0].text.strip()
        com['comment'] = comments[index].select('.short')[0].text.strip()
        result.append(com)

def get_all_page(url, result):
    for i in range(10):
        next_page = url + '?start=' + str(i * 20)
        get_one_page(next_page, result)


def write_to_file(result):
    with open('result/《头号玩家》短评.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['user', 'time', 'comment']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        try:
            writer.writerows(result)
        except Exception as e:
            print(e)



def main():
    url = 'https://movie.douban.com/subject/4920389/comments'
    result = list()
    get_all_page(url, result)
    write_to_file(result)


main()
