#-*- coding:utf-8 -*-
import pymysql
import openpyxl

'''    数据库存储影片信息'''
#'''
# 打开数据库连接
con = pymysql.connect("localhost","root","lixue123","shujukexue" )
cur = con.cursor()

#创建数据表
sql = 'create table movie_info(id int,name varchar(50),score float,five float,four float,three float,two float,one float,tag varchar(20),dirtor varchar(50),actor1 varchar(50),actor2 varchar(50),actor3 varchar(50),url varchar(50))'
cur.execute(sql)

#打开文件
wb = openpyxl.load_workbook('data_s\movie.xlsx')
#选择数据表
sheet = wb.get_sheet_by_name('Sheet')
#获取每行的单元值
for row in sheet.rows:
    try:
        sql = "insert into movie_info values ('%s', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d')" %\
            (row[0].value,row[1].value,row[2].value,row[3].value,row[4].value,row[5].value,row[6].value,row[7].value,row[8].value,row[9].value,row[10].value,row[11].value,row[12].value,row[13].value)
        print(sql)
        cur.execute(sql)
        con.commit()
    except:
        pass
    con.commit()

sql = 'create table people(name varchar(30),movie0 int(7),movie1 int(7),movie2 int(7),movie3 int(7),movie4 int(7),movie5 int(7),movie6 int(7),movie7 int(7),movie8 int(7),movie9 int(7))'
cur.execute(sql)
con.commit()
con.close()
print('数据导入完成')
