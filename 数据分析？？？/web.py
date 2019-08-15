import Wash_Data
import give_movie
import cgi

#实例化
if __name__ == '__main__':
    user_id = input("账号：")
    num = eval(input("推荐数量："))
    if num > 10 or num <= 0:
        num  = 10
    web = give_movie.give_movie()
    movie = web.get_movie(pathU="people_movie.txt",userID=user_id, N=num)
    if movie == None:
        print("查无此人！")
    else:
        for i in movie:
            print(i[0])