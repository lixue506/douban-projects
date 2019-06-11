#-*- coding:utf-8 -*-
import matplotlib
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D
from pylab import mpl
import pandas as pd
import numpy as np



#设置字体
mpl.rcParams['font.sans-serif'] = ['SimHei']
movie = pd.DataFrame(pd.read_excel(r'data_s/movie.xlsx'))
matplotlib.style.use('ggplot')
#计算平均分
score = movie.groupby(movie['类型']).mean()

#统计
kind_movie = {}#字典形式
sum = movie.groupby(movie['类型']).size()
for i in sum.index:
    kind_movie[i] = sum[i]

#每种类型电影五星好评相对比
for i in score.keys()[2:]:
    pd.DataFrame(score[i],index=kind_movie.keys()).plot.pie(subplots=True,autopct='%.2f')
    plot.show()


#散点图 探索评分与评星比例的关系
for i in score.keys()[2:]:
    plot.scatter(score['评分'],score[i])
    plot.xlim(0, 10)
    plot.ylim(0, 1)
    plot.title(i)
    plot.show()

#柱状图 各平均分的柱状图
pd.DataFrame(score['评分'],index = kind_movie.keys()).plot(color='green',kind = 'bar')
plot.show()

# 饼状图   以类型分的饼状图
pd.DataFrame(kind_movie.values(),index = kind_movie.keys()).plot.pie(subplots=True,autopct='%.2f')
plot.show()

# 柱状图   以类型分的柱状图
pd.DataFrame(kind_movie.values(),index = kind_movie.keys()).plot(color='green',kind = 'bar')
plot.show()


#
# #三维曲面图
# fig = plot.figure()
# ax = Axes3D(fig)
# for i in score.keys()[2:]:
#     X, Y = np.meshgrid(score['评分'], score[i])
#     R = np.sqrt(X**2 + Y**2)
#     Z = np.sin(R)
#     ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')
#     plot.title(i)
#     plot.show()