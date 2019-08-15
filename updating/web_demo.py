#-*- coding:utf-8 -*-
from math import *
import pymysql
import openpyxl
from flask import Flask,render_template
import Wash_Data
import cgi

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index.html', method=['get'])
def show():
    #接收前端数据
    form = cgi.FieldStorage()
    user_id = form.getvalue('user_id')
    T_true = Wash_Data.get_friend()
    if user_id in T_true.empty_people.keys():

        for i in T_true.empty_people[user_id]:
            print(i)
        print("用户未看过任何一部电影，无法得知该用户喜好！")
    elif user_id in T_true.data.keys():
        film = T_true.get_movie(user_id)
        for i in film.keys():
            print('电影名称:' + film[i][1][1] + ' 电影评分：' + str(film[i][1][2]) + ' 五星比：' + str(film[i][1][3:8]) + ' 类型：' + film[i][1][8] + '导演：' + film[i][1][9] + ' 演员：' + str(film[i][1][10:13]) + ' 网址: ' + film[i][1][13])
        sum, save_score, save_tag = T_true.analyze_cus(user_id)
        print('共看 ' + str(sum) + '部电影')
        print('评分情况：' + str(save_score))
        print('电影类型：' + str(save_tag))

    else:
        print("查无此人！")
    return render_template('show_movie.html')




if __name__ == '__main__':
    app.run()
