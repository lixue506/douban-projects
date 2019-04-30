# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 20:25:45 2019

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

def parser_html(html):
    soup = BeautifulSoup(html, "html.parser")
    data = soup.find('div', attrs={'class':"", 'id':"movie"}).find_all('a')[1]
    href = data.attrs['href']
    #用户常居地
    home = soup.find('div', attrs={'class':"user-info"})
    homes = re.findall(r'\S+',home.text)
#    a = str(homes[3])
#    print(a[:10])

    #正则匹配出电影数
    sum = data.text
    sum = int(re.findall(r'\d+', sum)[0])
    for i in range(0, 2, 1):#sum+1
        final_href = href+"?start=" + str(i) #控制翻页
        son_html = get_url(final_href)
        parser_son_html(son_html,homes)
        time.sleep(1)#爬得太多，控制速度

def parser_son_html(html,peo_info):
    soup = BeautifulSoup(html, "html.parser")
    names = soup.find_all('li', attrs={'class': 'title'})
    stars = soup.find('div',attrs={'class': "grid-view"})
    star = re.findall(r'<span class="rating\d+-t"></span>', str(stars))
    i = 0
    with open("people_movie.txt",'a',encoding="utf-8") as da:
        info = str(peo_info[3])
        final_info = info[:10]
#        print(peo_info[0]+peo_info[1]+', '+peo_info[2]+', 加入时间：'+final_info+';  ')
        da.write(peo_info[0]+peo_info[1]+', '+peo_info[2]+', 加入时间：'+final_info+';  ')
        for na in names:
            name = na.find('em').text
            final_name = re.findall(r'\S+',name)
            num = re.findall(r'\d+', star[i])
            da.write(final_name[0]+':'+num[0]+';')
#            print(final_name[0]+':'+num[0],end=';')
            i = i+1

if __name__ == "__main__":
    
#    final_url = 'https://www.douban.com/people/travelbao/'
    
    f = open("people_names.txt",'r',encoding="utf-8")   
    line = f.readline()
    line = line[:-1]
    final_url = re.findall(r'\:\S+', line)
    final_url = final_url[0]
    final_url = final_url[1:]
    html = get_url(final_url)
    parser_html(html)
    while line:
        line = f.readline()
        line = line[:-1]
        final_url = re.findall(r':\S+', line)
        final_url = final_url[0]
        final_url = final_url[1:]
        html = get_url(final_url)
        parser_html(html)   
    f.close()


