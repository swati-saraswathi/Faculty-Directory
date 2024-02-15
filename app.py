from flask import Flask, url_for, request, session, g
from flask.templating import render_template
from werkzeug.utils import redirect
from database import get_database
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.teardown_appcontext
def close_database(error):
    if hasattr(g, 'crudapplication_db'):
        g.crudapplication_db.close()

def get_current_user():
    user = None
    if 'user' in session:
        user = session['user']
        db = get_database()
        user_cur = db.execute('select * from emp where email = ?', [user])
        user = user_cur.fetchone()
    return user

@app.route('/')
def index():
    user = get_current_user()
    db = get_database()
    emp_cur = db.execute('select * from emp')
    allemp = emp_cur.fetchall()
    return render_template('home.html', user = user, allemp=allemp)

@app.route('/login', methods = ["POST", "GET"])
def login():
    user = get_current_user()
    error = None
    db = get_database()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_cursor = db.execute('select * from users where email = ?', [email])
        user= user_cursor.fetchone()
        if user:
            if check_password_hash(user['password'], password):
                session['user'] = user['email']
                return redirect(url_for('dashboard',email = user['email']))
            else:
                error = "Username or Password did not match, Try again."
        else:
            error = 'Username or password did not match, Try again.'        
    return render_template('login.html', loginerror = error, user = user)

@app.route('/register', methods=["POST", "GET"])
def register():
    user = get_current_user()
    db = get_database()
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        designation = request.form['designation']
        education = request.form['education']
        email = request.form['email']
        phonenumber = request.form['phonenumber']
        address = request.form['address']
        project = request.form['project']
        experience = request.form['experience']
        hashed_password = generate_password_hash(password)
        dbuser_cur = db.execute('select * from users where email = ?', [name])
        existing_username = dbuser_cur.fetchone()
        if existing_username:
            return render_template('register.html', registererror = 'Username already taken , try different username.')
        db.execute('insert into users ( email, password) values (?, ?)',[email, hashed_password])
        db.execute('insert into emp (name,designation,Education,email,phone,address,total_projects,years_of_experience) values (?, ?, ?, ?, ?, ?, ?, ?)',[name, designation, education,email, phonenumber, address, project,experience])
        db.commit()
        return redirect(url_for('index'))
    return render_template('register.html', user = user)

@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    db = get_database()
    if 'user' in session:
        emp_cur = db.execute('select * from emp')
        allemp = emp_cur.fetchall()
    return render_template('dashboard.html', user = user, allemp=allemp)

@app.route('/singleemployee/<int:empid>')
def singleemployee(empid):
    user = get_current_user()
    db = get_database()
    emp_cur = db.execute('select * from emp where empid = ?', [empid])
    single_emp = emp_cur.fetchone()
    return render_template('singleemployee.html', user = user, single_emp = single_emp)

@app.route('/fetchone/<int:empid>')
def fetchone(empid):
    user = get_current_user()
    db = get_database()
    emp_cur = db.execute('select * from emp where empid = ?', [empid])
    single_emp = emp_cur.fetchone()
    return render_template('updateemployee.html', user = user, single_emp = single_emp)

@app.route('/updateemployee' , methods = ["POST", "GET"])
def updateemployee():
    user = get_current_user()
    if request.method == 'POST':
        empid = request.form['empid']
        name = request.form['name']
        designation = request.form['designation']
        education = request.form['education']
        email = request.form['email']
        phonenumber = request.form['phone']
        address = request.form['address']
        project = request.form['project']
        experience = request.form['experience']
        db = get_database()
        db.execute('update emp set name=?,designation=?,Education=?,email=?,phone=?,address=?,total_projects=?,years_of_experience=? where empid = ?', [name, designation, education,email, phonenumber, address, project,experience,empid])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('updateemployee.html', user = user)

@app.route('/deleteemp/<int:empid>', methods = ["GET", "POST"])
def deleteemp(empid):
    user = get_current_user()
    if request.method == 'GET':
        db = get_database()
        db.execute('delete from emp where empid = ?', [empid])
        db.commit()
        return redirect(url_for('index'))
    return render_template('home.html', user = user)

@app.route('/logout')
def logout():
    session.pop('user', None)
    render_template('home.html')

if __name__ == '__main__':
    app.run(debug = True)