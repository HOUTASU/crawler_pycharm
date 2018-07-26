import requests
from bs4 import BeautifulSoup


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
        chinese_title = titlt_list[0].text
        info = m.select('.info .bd p')[0].text

        quote = m.select('.quote .inq')
        if quote:
            q = quote[0].text
        movie = list()
        movie.append(english_title)
        print("rank:{} name:{}".format(rank, chinese_title))
        result.append(movie)

    if soup.select('.next a'):
        asoup = soup.select('.next a')[0]['href']
        original_url = 'https://movie.douban.com/top250'
        Next_page = original_url + asoup
        douban_crawer(Next_page, result)
    return result


# //*[@id="content"]/div/div[1]/ol/li[1]/div/div[2]/div[1]/a/span[1]

url = 'https://movie.douban.com/top250'
result = list()
re = douban_crawer(url, result)
