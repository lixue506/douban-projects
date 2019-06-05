#-*- coding:utf-8 -*-
import Wash_Data


class give_movie():
    give = []
    def get_movie(self, pathU, userID, N):
        #实例化类
        movie = Wash_Data.get_friend()
        #字典，所有用户的电影
        data = movie.Parse_People_Movie(pathU)
        #判断用户时候存在
        if userID not in data.keys():
            return None
        #取出电影
        for i in movie.top_simliar(userID):#相似用户
            user_two = data[i[0]] #相似用户id
            for j in user_two.keys():#相似用户电影
                if j not in data.keys() and j not in self.give:
                    #找出评分前n的电影
                    score = user_two[j]
                    tu = (j,score)
                    if len(self.give) < N:
                        self.give.append(tu)#找出电影
                    elif len(self.give) == N:
                        sorted(self.give, key = lambda give:give[1])#默认升序
                        if score > self.give[0][1] and tu not in self.give:
                            self.give[0] = tu
        #列表（元组）
        return self.give
