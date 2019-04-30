import requests
import json
from bs4 import BeautifulSoup


num=0        #设定爬取次数
user_all=[]  #存放本次运行的用户

#解析网页
def get_url(url): #获取链接内容
    try:
        header_info = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
        }
        r = requests.get(url, hearders = header_info)
        if r.status_code == 200:
            return r.text
    except:
        print("爬取失败")
        return None

# 获取用户关注人的信息
def get_follower(userID):
    url = 'https://www.douban.com/people/' + userID + '/_contacts'
    html = get_url(url)
    soup = BeautifulSoup(html,'html.parser')
    url_data = soup.find_all('a',attrs = {'class':'nbg'})
    lists[follow_url['href'] for follow_url in url_data]
    return lists

#递归爬去所有用户url__token
def digui(list):
    global num                   #全局变量，爬取多少次
    temporary = []               #存放本次爬取的用户名
    for url in list:
        if (num == 10):
            return 0
        else:
            num = num + 1
            print(num)
            list = get_follower(url)
            user_all.extend(list)             #全局变量，存放所有爬取的用户名
            temporary.extend(list)           #存放本次爬取的用户名
            print(list)
    digui(temporary)                         #递归爬取

#解析用户信息
def parser_html(html):
    soup = BeautifulSoup(html, 'html,parser')
    name = soup.find('h1').text
    address = soup.find('div',attrs={'class':"user-info"}).find('a').text
    userid = soup.find('div', attrs={'class':"pl"}).text
    href = soup.find('div',attrs={'class':" ", 'id':"movie"}).find_all('a',attrs={'target':'_blank'})[1].text
    

#保存

#主函数
if __name__=='__main__':
    first_header = 'https://www.douban.com/people/travelbao/'
