import requests
from bs4 import BeautifulSoup
import time


def get_html(url, result):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    r = requests.get(url, headers)
    print(r.status_code)
    r.encoding = 'gbk'
    html = r.text
    parser_html(html, result)


def parser_html(html, result):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        title = soup.select('.bookname h1')[0].text
    except:
        print('已到最后一页')
        return ''

    content = soup.select('#content')[0].text.strip().replace('\xa0', '')

    result.append(content)

    next = soup.select('.bottem1 a')[3]['href']
    url = 'https://www.bequge.com'
    next_page = url + next
    get_html(next_page, result)


def main():
    url = 'https://www.bequge.com/11_11147/13169261.html'
    result = list()
    get_html(url, result)
    with open(r'..\result\黎明之剑.txt', 'w', encoding='utf-8') as f:
        for i in result:
            f.write(i)


if __name__ == '__main__':
    main()
