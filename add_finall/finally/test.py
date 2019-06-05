import Wash_Data
import give_movie
from flask import Flask,render_template
import cgi

app = Flask(__name__)
@app.route('/')
def guide():
    return render_template('index.html')

def
    #接收前端数据
    form = cgi.FieldStorage()
    user_id = form.getvalue('user_id')
    num = form.getvalue('num')
    if num > 10 or num <= 0:
        num  = 10
    #实例化give_movie
    web = give_movie.give_movie()
    movie = web.get_movie(pathU="people_movie.txt",userID=user_id, N=num)
@app.route('/show_movie')
@app.route('/show_movie/<movie>')
def show_movie(movie = None):
    return render_template('show_movie.html',R_movie=movie)


if __name__ == '__main__':
    app.run()




# #接收前端数据
# form = cgi.FieldStorage()
# user_id = form.getvalue('user_id')
# num = form.getvalue('num')
# if num > 10 or num <= 0:
#     num  = 10
#实例化