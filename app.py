from flask import Flask, request, render_template, redirect, url_for
from mysql import MySQL
from main import Student

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py', mode='r')



mysql = MySQL()

@app.before_request
def before_request():
    mysql.connect()

@app.teardown_request
def teardown_request(exception):
    mysql.disconnect()

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sql = "select * from user where username=%s and password=%s"
        params = (username, password)
        result = mysql.execute(sql, params, True)
        if result:
            return redirect(url_for('menu'))
        else:
            error = '用户名或密码错误，请重新输入！'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')


@app.route('/register',method=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sql = "insert into user(username,password)values(%s,%s) "
        params = (username,password)
        mysql.execute(sql,params)
        return redirect(url_for('login'))

@app.route('/add',method=['GET','POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    elif request.method == 'POST':
        id = request.form['id']
        classe = request.form['classe']
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        score = request.form['score']
        sql = "insert into students_data(id,classe,name,age,gender,score)values(%s,%s,%s,,%s,%s,%s)"
        params = (id,classe,name,age,gender,score)
        mysql.execute(sql,params)
        return redirect(url_for('menu'))

@app.route('/delete',method=['GET','POST'])
def delete():
    if request.method == 'GET':
        return render_template('delete.html')
    elif request.method == 'POST':
        id =  request.form['id']
        sql = "delete from students_data where id=%s"
        params = (id,)
        mysql.execute(sql,params)
        return  redirect(url_for('menu'))

@app.route('/update',method=['GET','POST'])
def update():
    if request.method == 'GET':
        return render_template('add.html')
    elif request.method == 'POST':
        id = request.form['id']
        classe = request.form['classe']
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        score = request.form['score']
        sql = "update students_data set id=%s,classe=%s,name=%s,age=%s,gender=%s,score=%s where id=%s"
        params = (id, classe, name, age, gender, score,id)
        mysql.execute(sql, params)
        return redirect(url_for('menu'))

@app.route('/query',method = ['GET','POST'])
def query():
    if request.method == 'POST':
        keyword =request.form['keyword']
        sql = "select from students_data where id=%s or name like %s"
        params = (keyword,f"%{keyword}%")
        results = mysql.execute(sql,params,True)
        students = [Student(*results) for result in results]
        return  render_template('query.html',students=students)
    else:
        return render_template('query.html')

@app.route('/menu')
def menu():
    return  render_template('menu.html')

if __name__ =='__main__':
    app.run()



