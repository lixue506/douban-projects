# -*- coding: utf-8 -*-
import xlrd
import time
import requests
from bs4 import BeautifulSoup


def get_son_html(url):
    try:
        d = {
            'Cookie': 'bid=JoOO5Fbfy_U; __yadk_uid=HKvC8XvM5dNKhhV1SL6zGyRVjrAjrfU6; ll="118222"; douban-profile-remind=1; douban-fav-remind=1; ct=y; _vwo_uuid_v2=DBBFD1C4D4352E321CF39AA05ECDBC25C|ec2df2e7c16cc03c0576e19027669a33; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1556023088%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; ap_v=0,6.0; ps=y; dbcl2="193741190:MGOdDJNKEdo"; ck=cz6U; _pk_id.100001.4cf6=0f01e131a17d1b6d.1552918691.7.1556024644.1556019512.; _pk_ses.100001.4cf6=*; __utma=30149280.819158214.1555853957.1556019512.1556023088.5; __utmb=30149280.0.10.1556023088; __utmc=30149280; __utmz=30149280.1555943362.2.2.utmcsr=blog.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/datacastle/article/details/78812575; __utma=223695111.1261872010.1552918691.1556019512.1556023088.7; __utmb=223695111.0.10.1556023088; __utmc=223695111; __utmz=223695111.1556016662.5.4.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; push_noty_num=0; push_doumail_num=0',
            'User Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"}
        r = requests.get(url=url, headers=d)
        if r.status_code == 200:
            return r.text
    except:
        print("爬取失败")
        return None

#定位爬取
def params_son_html(html):
    soup = BeautifulSoup(html, "html.parser")
    #name
    name = soup.find('span', attrs={'property':"v:itemreviewed"})
    print("name: " + name.text)
    #rate
    rate = soup.find('strong', attrs={'class':"ll rating_num", 'property':"v:average"})
    # tag
    tags = soup.find_all('span', attrs={'property': "v:genre"} )
    # 五星评分
    star = soup.find_all('span', attrs={'class': "rating_per"})
    #dirctor
    dirctor = soup.find('a',attrs={'rel':"v:directedBy"})
    # 写入文件


def get_url():
    with open('save_url.txt','r',encoding='utf-8') as f:
        while True:
            url = f.readline().strip('\n')#去回车
            #print(url)
            if url == '':
                break
            else:
                html = get_son_html(url)
                params_son_html(html)
            time.sleep(1)#控制速度，差点封IP
    f.close()
    print("爬去完成")

if __name__ == '__main__':
    get_url()