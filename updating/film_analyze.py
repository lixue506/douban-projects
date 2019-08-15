#-*- coding:utf-8 -*-
import pymysql
import matplotlib
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D
from pylab import mpl
import pandas as pd
import numpy as np



def film(name):
    # 打开数据库连接
    con = pymysql.connect("localhost", "root", "lixue123", "shujukexue")
    cur = con.cursor()

    # 创建数据表
    sql = 'select name,tag,score,five,four,three,two,one from movie_info where name like ' + '"%' + name + '%"'
    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) == 0:
        print("查无此电影！")
        return
    else:
        #分析电影相对于与所有电影的平均分
        #相对于此标签中所有电影的平均分
        for row in rows:
            sql = 'select score,tag from movie_info'
            cur.execute(sql)
            cols = cur.fetchall()
            per_score = 0.0
            tag_score = 0.0
            tag_num = 0
            for i in cols:
                per_score += i[0]
                if i[1] == row[1]:
                    tag_score += i[0]
                    tag_num += 1
            print('电影名称：' + str(row[0]))
            print('电影评分：' + str(row[2]))
            if per_score/len(cols) > row[2]:
                print('低于平均分，电影平均分为' + str(per_score/len(cols)))
            else:
                print('高于平均分，电影平均分为' + str(per_score / len(cols)))
            if tag_score/tag_num > row[2]:
                print('低于同类型电影平均分，同类型电影平均分为' + str(tag_score / tag_num))
            else:
                print('高于同类型电影平均分，同类型电影平均分为' + str(tag_score / tag_num))
            print('电影类型：' + str(row[1]))
            print('电影五星率：'+ str(row[3]) + ',' + str(row[4]) + ',' + str(row[5]) + ',' + str(row[6]) + ',' + str(row[7]))

            # 设置字体
            mpl.rcParams['font.sans-serif'] = ['SimHei']
            movie = pd.DataFrame(pd.read_excel(r'data_s\movie.xlsx'))
            matplotlib.style.use('ggplot')
            # 五星比
            index_name= ['五星','四星','三星','二星','一星']
            pd.DataFrame(row[3:8], index=index_name).plot(color='green', kind='bar')
            plot.title('五星评价分布')
            plot.show()
            #评分
            gride = ['平均分','得分','类型平均分']
            pd.DataFrame([per_score/len(cols), row[2], tag_score/tag_num],index=gride).plot(color='green', kind='bar')
            plot.title('得分比较')
            plot.show()


    con.close()


if __name__=='__main__':
    name = input('请输入电影名称：')
    film(name)
