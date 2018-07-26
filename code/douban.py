import requests
from bs4 import BeautifulSoup
import csv


def douban_crawer(url, result):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    movie_list = soup.select('.grid_view li')
    for m in movie_list:
        rank = m.select('em')[0].text
        titlt_list = m.select('.title')
        if (len(titlt_list)) > 1:
            english_title = titlt_list[1].text.strip().strip('/').replace('\xa0', '')
        else:
            english_title = 'None'
        chinese_title = titlt_list[0].text.strip()
        info = m.select('.info .bd p')[0].text.strip()

        quote = m.select('.quote .inq')
        if quote:
            q = quote[0].text
        movie = {}
        movie['rank'] = rank
        movie['chinese_title'] = chinese_title
        movie['english_title'] = english_title
        movie['info'] = info
        result.append(movie)

    if soup.select('.next a'):
        asoup = soup.select('.next a')[0]['href']
        original_url = 'https://movie.douban.com/top250'
        Next_page = original_url + asoup
        douban_crawer(Next_page, result)
    return result


def write_to_file(result):
    with open(r'..\result\Top250.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['rank', 'chinese_title', 'english_title', 'info']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        try:
            writer.writerows(result)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    url = 'https://movie.douban.com/top250'
    result = list()
    result = douban_crawer(url, result)
    write_to_file(result)
