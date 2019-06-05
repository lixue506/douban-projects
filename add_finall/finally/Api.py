import predict_Score
import data_Wash


def Setup(pathU,pathM):
    '''
        input:movie path and userdata path to get formated data
    '''
    data_Wash.set_up(pathU,pathM)


def doPredict(username,moviename):
    '''
        usage : doPredict(username,moviename)
            when you use it,it will give you a predict
    '''
    fScore = predict_Score.doPredict(username,moviename)
    if(fScore - int(fScore)>0.5):
        return int(fScore + 0.5)
    else:
        return int(fScore)

if __name__ == '__main__':
    '''
        for example:
    '''
    Setup('./people_movie.txt','./save_movies.txt')
    print('modle : 用户：157353420 电影：飞驰人生 预测分数：'+str(doPredict('157353420','飞驰人生')))