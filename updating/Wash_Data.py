#-*- coding:utf-8 -*-
from math import *
import pymysql
import openpyxl


class get_friend():

    data = {}#存放每位用户评论的电影和评分
    empty_people = {}

    def __init__(self):
        # 打开数据库连接
        con = pymysql.connect("localhost", "root", "lixue123", "shujukexue")
        cur = con.cursor()
        # 创建数据表
        # sql = 'create table movie_info(id int,name varchar(50),score float,five float,four float,\
        #         three float,two float,one float,tag varchar(20),dirtor varchar(50),actor1 varchar(50),\
        #         actor2 varchar(50),actor3 varchar(50),url varchar(50))'
        # cur.execute(sql)
        #
        # # 打开文件
        # wb = openpyxl.load_workbook('data_s\movie.xlsx')
        # # 选择数据表
        # sheet = wb.get_sheet_by_name('Sheet')
        # # 获取每行的单元值
        # for row in sheet.rows:
        #     try:
        #         sql = "insert into movie_info values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
        #               (row[0].value, row[1].value, row[2].value, row[3].value, row[4].value, row[5].value, row[6].value,
        #                row[7].value, row[8].value, row[9].value, row[10].value, row[11].value, row[12].value,
        #                row[13].value)
        #         cur.execute(sql)
        #         con.commit()
        #     except:
        #         pass
        #     con.commit()
        # con.commit()

        # 处理空数据
        sql = 'select * from movie_info order by score desc,five desc,four desc,three desc,two desc,one desc limit 10'
        cur.execute(sql)
        rows = cur.fetchall()
        row = [i for i in rows]


        with open('data_s\people_movie.txt','r', encoding='UTF-8') as file:
            for line in file.readlines():
                give_score = '0123456789'
                movie_score = {}
                new = line.split(';')
                #未看电影的客户存放在数据库，否接放在列表
                if new[3] == '\n':#判断申请账号，但未观看任何一部电影的用户
                    self.empty_people[new[1]] = row
                    # continue
                    # sql = "insert into people values ('%s','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d')" %\
                    #       (new[1],row[0][0],row[1][0],row[2][0],row[3][0],row[4][0],row[5][0],row[6][0],row[7][0],row[8][0],row[9][0])
                    # cur.execute(sql)
                    # con.commit()
                    # self.empty_people[new[1]] = row
                else:
                    for i in new[3].split('，'):
                        if i == '\n' or i == '':
                            continue
                        if not i[:-2] in movie_score.keys() and i[-1:] in give_score:
                            movie_score[i[0:-2]] = i[-1:]#更新个人观看字典
                    if not new[1] in self.data.keys():
                        self.data[new[1]] = movie_score
        file.close()
        con.close()


    #工具函数计算欧氏距离
    def Euclidean(self,userID, user_two):
        #取出两位用户评论过的电影和评分
        user1_data = self.data[userID]
        user2_data = self.data[user_two]
        distance = 0.0
        #找到两位用户都评论过的电影，并计算欧式距离
        for key in user1_data.keys():
            if key in user2_data.keys():#注意，distance越大表示两者越相似
                if user1_data[key]=='\n' or user2_data[key]=='\n':
                    continue
                distance += (float(user1_data[key])-float(user2_data[key]))**2
        return 1/(1+sqrt(distance))#这里返回值越小，相似度越大

    #计算某个用户与其他用户的相似度
    def top_simliar(self, userID):
        res = []
        for userid in self.data.keys():
            if not userid == userID: #排除与自己计算相似度
                simliar = self.Euclidean(userID,userid)
                res.append((userid,simliar))
        get_people = sorted(res, key = lambda val:val[1])[:5]
        # 返回相似用户的ID以及相似度
        return get_people


    #用户分析
    def analyze_cus(self,userID):
        # 打开数据库连接
        con = pymysql.connect("localhost", "root", "lixue123", "shujukexue")
        cur = con.cursor()

        #取出该用户所看电影
        if userID not in self.data.keys():
            return None
        saw_movie = self.data[userID]
        sum = 0
        save_score = {'0':0,'1':0,'2':0,'3':0,'4':0,'5':0}
        save_tag = {'其它':0}

        for n_movie in saw_movie.keys():
            sql = 'select tag,score from movie_info where name like ' + str('"%' + n_movie + '%"')
            cur.execute(sql)
            cols = cur.fetchall()
            if len(cols) == 0:
                sum += 1
                save_tag['其它'] += 1
                save_score[saw_movie[n_movie]] += 1
            else:
                for i in cols:
                    sum += 1
                    if i[0] in save_tag.keys():
                        save_tag[i[0]] += 1
                    else:
                        save_tag[i[0]] = 0
                    save_score[saw_movie[n_movie]] += 1
        con.close()
        return sum,save_score,save_tag
        #找出用户好评情况，所看电影类型趋向

    #找出推荐电影存入数据库
    def get_movie(self,userID):
        # 打开数据库连接
        con = pymysql.connect("localhost", "root", "lixue123", "shujukexue")
        cur = con.cursor()

        simliar_people = self.top_simliar(userID)
        r_film = {}

        for man in simliar_people:
            #相似用户的电影字典 man = (用户id,相似率)
            man_movie = self.data[man[0]]
            for movie in man_movie.keys():
               if movie not in self.data[userID].keys():
                    sql = 'select * from movie_info where name like ' + str('"%' + movie + '%"')
                    cur.execute(sql)
                    cols = cur.fetchall()
                    if len(cols) == 0:
                       continue
                    else:
                        for g_score in cols:
                            if len(r_film) < 10:
                                r_film[g_score[0]] = g_score
                            else:
                                #找出推进按电影中最低分,temp[0]:电影序号，temp[1]:电影得分
                                temp = ['', 10]
                                for r_name in r_film.keys():
                                    son_dict = r_film.get(r_name)
                                    #选择高评分电影
                                    if son_dict[2] < temp[1]:
                                        temp[0] = r_name
                                if g_score[2] > temp[1]:
                                    r_film.pop(temp[0])
                                    r_film[g_score[0]] = g_score
        con.close()
        return r_film

