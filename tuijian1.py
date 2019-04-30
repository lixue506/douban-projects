import sys
import math
from texttable import Texttable
import importlib

#计算余弦距离
def getCosDist(user1, user2):

    sum_x = 0.0
    sum_y = 0.0
    sum_xy = 0.0
    for key1 in user1:
        for key2 in user2:
            if key1[0] == key2[0]:  #key1[0]表示电影id，key1[1]表示用户1对它的评分, 如果是两个用户评价的同一id的电影
                sum_x += key1[1] * key1[1]
                sum_y += key2[1] * key2[1]
                sum_xy += key1[1] * key2[1]
    if sum_xy == 0.0:
        return 0
    demo = math.sqrt(sum_x * sum_y)
    return sum_xy / demo

#读取文件，读取以行为单位，每一行是列表里的一个元素
def readFile(filename):
    contents = []
    f = open(filename, "rb")
    contents = f.readlines()
    f.close()
    return contents

#数据格式化为二维数组
def getRatingInfo(ratings):
    rates = []
    for line in ratings:
        rate = line.split("\t".encode(encoding="utf-8"))
        rates.append([int(rate[0]), int(rate[1]), int(rate[2])])
    return rates

#生成用户评分数据结构
def getUserScoreDataStructure(rates):

    #userDict[2]=[(1,5),(4,2)]…. 表示用户2对电影1的评分是5，对电影4的评分是2
    #itemUser[12]=[5,10] 表示给item=12的电影评分的有用户id=5,10
    userDict = {}
    itemUser = {}
    for k in rates:
        user_rank = (k[1], k[2])  #user_rank是元组：item 和 评分
        if k[0] in userDict:
            userDict[k[0]].append(user_rank)
        else:
            userDict[k[0]] = [user_rank]

        if k[1] in itemUser:
            itemUser[k[1]].append(k[0])
        else:
            itemUser[k[1]] = [k[0]]
    return userDict, itemUser

#计算与指定用户最相近的邻居 ,返回所有邻居的相似度

"""
用户userId评分的电影: [(23, 5), (100,4), (230,5), (299,2)]
邻居k 评分的电影: [(23, 4), (234, 5), (230, 2)]
getCosDist(user1, user2)为计算两个用户的的余弦距离
"""
def getNearestNeighbor(userId, userDict, itemUser):
    neighbors = []
    for item in userDict[userId]:  #item为用户user_id评分过的电影 (item_id, 评分)
        for neighbor in itemUser[item[0]]:  #item[0]为item_id, itemUser[item[0]]为所有评分过item[0]的用户集合
            if neighbor != userId and neighbor not in neighbors:
                neighbors.append(neighbor)
    neighbors_dist = []
    for neighbor in neighbors:  #neighbors为所有和用户userId评分过相同电影的用户集合
        dist = getCosDist(userDict[userId], userDict[neighbor])  #比较userId和邻居neighbor的相似度
        neighbors_dist.append([dist, neighbor])
    neighbors_dist.sort(reverse = True)
    return neighbors_dist

#使用UserFC进行推荐，输入：文件名,用户ID,邻居数量
def recommendByUserFC(filename, userId, k = 5):

    #读取文件
    contents = readFile(filename)

    #文件格式数据转化为二维数组
    rates = getRatingInfo(contents)  #rates是list, rates[0] 是用户id, rates[1]是item, rates[2]是评分

    #格式化成字典数据
    userDict, itemUser = getUserScoreDataStructure(rates)
    """
    userDict= { 50:[(1,5),(1084,4),(23,2)], 60:[(1,4)] }
    itemUser= { 1:[50,60,1,2], 1084:[50, 70] }
    userDict为用户对评分过的电影的dict，dict由元组组成; key为user_id
    itemUser为给电影item评分过的用户dict; key为item_id
    """

    #找邻居
    neighbors = getNearestNeighbor(userId, userDict, itemUser)[:10] #只需要相似度前5名的邻居
    print('neighbors:', neighbors) #(相似度， user_id)
    #建立推荐字典
    recommand_dict = {}
    for neighbor in neighbors:
        neighbor_user_id = neighbor[1]   #neighbor[1]是user_id
        movies = userDict[neighbor_user_id]
        for movie in movies:
            if movie[0] not in recommand_dict:
                recommand_dict[movie[0]] = neighbor[0]  #neighbor[0]是余弦距离，相似度;  movie[0]是item_id
            else:
                recommand_dict[movie[0]] += neighbor[0]  #保存该item_id的所有相似度之和

    #建立推荐列表
    recommand_list = []
    for key in recommand_dict:
        recommand_list.append([recommand_dict[key], key])  #(相似度， item_id)
    recommand_list.sort(reverse = True)
    user_movies = [k[0] for k in userDict[userId]]
    return [k[1] for k in recommand_list], user_movies, itemUser, neighbors  #k[1]为item_id

#获取电影的列表
def getMovieList(filename):
    contents = readFile(filename)
    movies_info = {}  #dict
    for movie in contents:
        single_info = movie.split("|".encode(encoding="utf-8"))  #把当前行按|分隔，保存成list
        movies_info[int(single_info[0])] = single_info[1:]  #将第0个元素作为key，第二个到最后作为value保存成字典dict返回
    return movies_info

#从这里开始运行
if __name__ == '__main__':

    importlib.reload(sys)

    #获取所有电影的列表
    movies = getMovieList("u.item")  #movies为dict
    recommend_list, user_movie, items_movie, neighbors = recommendByUserFC("u.data", 50, 80)  #用户id=50， 80个邻居
    print('recommend_list:', recommend_list[:20]) #推荐列表
    print('user_movie:', user_movie)
    #print('items_movie:', items_movie)
    #print('neighbors:', neighbors)

    neighbors_id=[ i[1] for i in neighbors]
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype(['t', 't', 't'])
    table.set_cols_align(["l", "l", "l"])
    rows=[]
    rows.append([u"movie name",u"release", u"from userid"])
    for movie_id in recommend_list[:20]:
        from_user=[]
        for user_id in items_movie[movie_id]:
            if user_id in neighbors_id:
                from_user.append(user_id)
        rows.append([movies[movie_id][0],movies[movie_id][1]," "])
    table.add_rows(rows)
    print (table.draw())
