# -*- coding: utf-8 -*-
# 爬取用户所看电影信息
import re
import time
import requests
from bs4 import BeautifulSoup

def get_url(url):
    try:
        d = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'}
        r = requests.get(url=url, headers=d)
        if r.status_code == 200:
            return r.text
    except:
        return None

def parser_html(html):
    soup = BeautifulSoup(html, "html.parser")
    data = soup.find('div', attrs={'class':"", 'id':"movie"}).find_all('a')[1]
    href = data.attrs['href']
    #正则匹配出电影数
    sum = data.text
    sum = int(re.findall(r'\d+', sum)[0])
    for i in range(0, sum+1, 15):
        final_href = href+"?start=" + str(i) #控制翻页
        son_html = get_url(final_href)
        parser_son_html(son_html)
        time.sleep(1)#爬得太多，控制速度

def get_name(url):
    htext = get_url(url)
    name = BeautifulSoup(htext, "html.parser").find('h1')
    name = name.find('span',attrs={'property':"v:itemreviewed"}).text
    return name

def parser_son_html(html):
    soup = BeautifulSoup(html, "html.parser")
    movie_space = soup.find_all( 'div', attrs={'class': "info"} )
    for movie in movie_space:
        son_url = movie.find('a')
        name_href = son_url.attrs['href']
        name = get_name( name_href )
        print(name)
        rate = re.findall(r'<span class="rating\d-t">',movie)
        rate = re.findall(r'\d',rate)
        print(rate)




if __name__ == "__main__":
    url = 'https://www.douban.com/people/travelbao/'
    html = get_url(url)
    parser_html(html)
