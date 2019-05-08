# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 21:53:05 2019

@author: qaz
"""

import re
import time
import requests
from bs4 import BeautifulSoup

def get_url(url):
    try:
        d = {
            'Cookie':'bid=nx6q2HX1XTc; douban-fav-remind=1; ll="118222"; douban-profile-remind=1; viewed="30376420"; ct=y; gr_user_id=99459bcb-2665-4a7c-9fc2-540df98d002c; ap_v=0,6.0; _vwo_uuid_v2=D19EDAFCF2010E40AE38DAF926B1A9A7C|51e5663e9afd68c8db94a1f6934e30d1; dbcl2="195525565:WapY4RsKcsE"; ck=umCg; push_noty_num=0; push_doumail_num=0; __utma=30149280.973968605.1543202989.1556331846.1556340330.17; __utmb=30149280.15.9.1556341913637; __utmc=30149280; __utmz=30149280.1556340330.17.9.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.19552',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'}
        r = requests.get(url=url, headers=d)
        if r.status_code == 200:
            return r.text
    except:
        print("爬取失败！")
        return None

def parser_html(html, url):
    soup = BeautifulSoup(html, "html.parser")
    href = url
    #正则匹配出电影数
    data = soup.find('span', attrs={'class':"count"})
    sum = int(re.findall(r'\d+',data.text)[0])
#    print(sum)

    for i in range(0, sum+1, 1): ##30改成sum+1
        final_href = href+"?start=" + str(i) #控制翻页
        son_html = get_url(final_href)
        parser_son_html(son_html)
        time.sleep(1)#爬得太多，控制速度

def parser_son_html(html):
    soup = BeautifulSoup(html, "html.parser")
    peo_href = soup.find('header', attrs={'class':'main-hd'}).find_all('a')[1]
    href = peo_href.attrs['href']
    name = peo_href.text
#    print(name+' : '+href) 
    with open("people_names.txt",'a',encoding="utf-8") as da:
            da.write(name+':'+href)
            da.write('\n')

if __name__ == "__main__":
#    url = 'https://www.douban.com/'
    url = 'https://movie.douban.com/subject/30163509/reviews'
    html = get_url(url)
    parser_html(html,url)























