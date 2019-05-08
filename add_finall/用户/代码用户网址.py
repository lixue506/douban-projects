# -*- coding:utf-8 -*-
import re
import time
import requests
from bs4 import BeautifulSoup

#存放所有用户的网址，避免重复使用集合
follower = set()
#解析网页
def get_url(url): #获取链接内容
    try:
        header = {
            "Cookie":'bid=JoOO5Fbfy_U; __yadk_uid=HKvC8XvM5dNKhhV1SL6zGyRVjrAjrfU6; douban-profile-remind=1; douban-fav-remind=1; ct=y; ps=y; _ga=GA1.2.819158214.1555853957; ll="108296"; ap_v=0,6.0; dbcl2="193741190:MGOdDJNKEdo"; ck=cz6U; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1556698303%2C%22https%3A%2F%2Fwww.douban.com%2Fpeople%2Fluqy%2F%22%5D; _vwo_uuid_v2=DBBFD1C4D4352E321CF39AA05ECDBC25C|ec2df2e7c16cc03c0576e19027669a33; push_noty_num=0; push_doumail_num=0; _pk_id.100001.4cf6=0f01e131a17d1b6d.1552918691.27.1556698374.1556692773.; _pk_ses.100001.4cf6=*; __utma=30149280.819158214.1555853957.1556692773.1556695830.25; __utmb=30149280.23.10.1556695830; __utmc=30149280; __utmz=30149280.1556616814.19.6.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=30149280.19374; __utma=223695111.1261872010.1552918691.1556692773.1556698303.27; __utmb=223695111.0.10.1556698303; __utmc=223695111; __utmz=223695111.1556698303.27.15.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/luqy/',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
        }
        r = requests.get(url,headers=header)
        if r.status_code == 200:
            return r.text
    except:
        print("爬取失败")
        return None

# 分析大v
def get_follow(html):
    soup = BeautifulSoup(html, "html.parser")
    data = soup.find('a', attrs={'target': "_self"})['href']
    date = soup.find('p',attrs={'class':"rev-link"}).find('a')
    sum = re.findall(r'\d+',date.text)
    date = date['href']
    return data,date,int(sum[0])

def save_to_file(urls):
    with open('follower.text', 'a') as f:
        for url in urls:
            f.write(url + '\n')
            print(url)
        print("个人完成")
    f.close()

# 提取连接，进入关注页面
def save_url(html):
    soup = BeautifulSoup(html, "html.parser")
    save_list = soup.find_all('a', attrs={'class': "nbg"})
    finall_list = []
    for url in save_list:
        print(url['href'])
        if url['href'] not in follower:
            follower.add(url['href'])
            finall_list.append(url['href'])
    if len(finall_list) == 0:
        return None
    else:
        save_to_file(finall_list)

#主函数
if __name__=='__main__':
    first_header = ['https://www.douban.com/people/minhuzi/', 'https://www.douban.com/people/travelbao/', 'https://www.douban.com/people/luoruisheng/',\
                     'https://www.douban.com/people/chaosinchaos/','https://www.douban.com/people/douban-time/','https://www.douban.com/people/juzixuancao/',\
                    'https://www.douban.com/people/LordBean/','https://www.douban.com/people/163296676/','https://www.douban.com/people/glaciergr/']
    for src in first_header:
        if src not in follower:
            follower.add(src)
            print(follower)
        html = get_url(src)
        data,date,sum = get_follow(html)
        html_get = get_url(data)
        save_url(html_get)
        time.sleep(1)
        print(sum)
        for start in range(0, sum+1, 70):
            finall_date = date + '?start=' + str(start)
            print(finall_date)
            html_get = get_url(finall_date)
            save_url(html_get)
            time.sleep(1)
