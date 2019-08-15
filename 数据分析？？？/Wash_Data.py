#-*- coding:utf-8 -*-
from math import *

class get_friend():

    data = {}#存放每位用户评论的电影和评分

    def Parse_People_Movie(self,path_customer):
        with open(path_customer,'r', encoding='UTF-8') as file:
            for line in file.readlines():
                give_score = '0123456789'
                movie_score = {}
                new = line.split(';')
                if len(new) <= 3:#判断申请账号，但未观看任何一部电影的用户
                    continue
                for i in new[3].split('，'):
                    if i == '\n':
                        continue
                    if not i[:-2] in movie_score.keys() and i[-1:] in give_score:
                        movie_score[i[0:-2]] = i[-1:]#更新个人观看字典
                if not new[1] in self.data.keys():
                    self.data[new[1]] = movie_score
        file.close()
        return self.data

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
        return get_people

