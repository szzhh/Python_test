# 这段代码爬取了豆瓣Top250的电影清单。去看看你有多少电影还没有看过呀

import requests
import time
from bs4 import BeautifulSoup

def get_douban_movies(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    # 电影信息在 class='hd' 的 div 标签里
    items = soup.find_all('div', class_='hd')
    for i in items:
        tag = i.find('a')
        # 取 a 标签里的第一个 class='title' 的内容为电影名
        name = tag.find(class_='title').text
        # a 标签上有链接
        link = tag['href']
        print(name, link)

url = 'https://movie.douban.com/top250?start={}'
urls = [url.format(num * 25) for num in range(10)]
for i in urls:
    get_douban_movies(i)
    time.sleep(1)
