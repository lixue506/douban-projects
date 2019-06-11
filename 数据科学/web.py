#-*- coding:utf-8 -*-
from math import *
import pymysql
import openpyxl
import Wash_Data
import matplotlib
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D
from pylab import mpl
import pandas as pd

#实例化
if __name__ == '__main__':

    T_true = Wash_Data.get_friend()

    user_id = input("账号：")

    if user_id in T_true.empty_people.keys():
        for i in T_true.empty_people[user_id]:
            print('电影名称:' + i[1] + ' 电影评分：' + str(i[2]) + ' 五星比：' + str(i[3:8]) + ' 类型：' + i[8] + '导演：' + i[9] + ' 演员：' + str(i[10:13]) + ' 网址: ' + i[13])
        print("用户未看过任何一部电影，无法得知该用户喜好！")
    elif user_id in T_true.data.keys():
        film = T_true.get_movie(user_id)
        #print(film)
        for i in film.keys():
            print('电影名称:' + film.get(i)[1] + ' 电影评分：' + str(film.get(i)[2]) + ' 五星比：' + str(film.get(i)[3:8]) + ' 类型：' + film.get(i)[8] + '导演：' + film.get(i)[9] + ' 演员：' + str(film.get(i)[10:13]) + ' 网址: ' + film.get(i)[13])
        sum, save_score, save_tag = T_true.analyze_cus(user_id)
        print('共看 ' + str(sum) + '部电影')
        print('评分情况：' + str(save_score))
        print('电影类型：' + str(save_tag))
        # 设置字体
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        matplotlib.style.use('ggplot')
        pd.DataFrame(save_score.values(), index=save_score.keys()).plot(color='green', kind='bar')
        plot.title('五星评价分布')
        plot.show()
        pd.DataFrame(save_tag.values(), index=save_tag.keys()).plot(color='green', kind='bar')
        plot.title('类型分布')
        plot.show()

    else:
        print("查无此人！")