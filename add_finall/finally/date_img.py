import matplotlib
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D
from pylab import mpl
import pandas as pd
import numpy as np
import pymysql
import openpyxl

#设置字体
mpl.rcParams['font.sans-serif'] = ['SimHei']
movie = pd.DataFrame(pd.read_excel(r'movie.xlsx'))

matplotlib.style.use('ggplot')
#计算平均分
score = movie.groupby(movie['类型']).mean()
Broken_line = []
# for i in range(23):
#     print(score[i:i+1]['评分'])
#统计
kind_movie = {}#字典形式
sum = movie.groupby(movie['类型']).size()
for i in sum.index:
    kind_movie[i] = sum[i]


'''
#三维曲面图
fig = plot.figure()
ax = Axes3D(fig)
for i in score.keys()[2:]:
    X, Y = np.meshgrid(score['评分'], score[i])
    R = np.sqrt(X**2 + Y**2)
    Z = np.sin(R)
    break
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')
plot.savefig('surface' + i)
plot.show()
'''
'''
#散点图 探索评分与评星比例的关系
for i in score.keys()[2:]:
    plot.scatter(score['评分'],score[i])
    plot.xlim(0, 10)
    plot.ylim(0, 1)
    plot.savefig(i)
    plot.show()
    break
'''
'''
#柱状图 各平均分的柱状图
pd.DataFrame(score['评分'],index = kind_movie.keys()).plot(color='green',kind = 'bar')
plot.savefig('score_histogram')
plot.show()
'''
'''
# 饼状图   以类型分的饼状图
pd.DataFrame(kind_movie.values(),index = kind_movie.keys()).plot.pie(subplots=True,autopct='%.2f')
plot.savefig('pie')
plot.show()
'''
'''
# 柱状图   以类型分的柱状图
pd.DataFrame(kind_movie.values(),index = kind_movie.keys()).plot(color='green',kind = 'bar')
plot.savefig('histogram')
plot.show()
'''

'''
# # 打开数据库连接
# con = pymysql.connect("localhost","root","lixue123","movie" )
# cur = con.cursor()
#
# #打开文件
# wb = openpyxl.load_workbook('movie.xlsx')
# #选择数据表
# sheet = wb.get_sheet_by_name('Sheet')
# #获取每行的单元值
# for row in sheet.rows:
#     try:
#         sql = "insert into info values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %\
#             (row[0].value,row[1].value,row[2].value,row[3].value,row[4].value,row[5].value,row[6].value,row[7].value,row[8].value,row[9].value,row[10].value,row[11].value)
#         print(row[0].value)
#         cur.execute(sql)
#         con.commit()
#     except:
#         pass
#     con.commit()
# con.commit()
# con.close()
# print('数据导入完成')]
'''