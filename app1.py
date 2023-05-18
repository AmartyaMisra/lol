from flask import Flask, render_template, flash, request
from flask import render_template
import sqlite3
# import requests
from flask import Flask
from flask import request,redirect,url_for,session,flash
from flask_wtf import FlaskForm
#from wtforms import TextField
app = Flask(__name__)
app.secret_key = "SecretKey"

@app.route("/")
def home():
    conn = sqlite3.connect('users.db')
    return "<h1>Welcome Page</h1>"

@app.route("/greet")
def greet():
    value = request.args.get('name')
    return render_template('greet.html', name = value)
@app.route("/index")
def index():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    user = cursor.fetchone()
    conn.close()
    if user:
            name = user[1]
            return f'Welcome, {name}!'
    #value = request.args.get('name')
    return render_template('index.html')

def create_users_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       username TEXT NOT NULL,
                       password TEXT NOT NULL)''')
    conn.commit()
    conn.close()
def create_couples_table():
    conn = sqlite3.connect('couples.db')
    cursor = conn.cursor()
    conn.execute('''CREATE TABLE IF NOT EXISTS couple
      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
      city TEXT NOT NULL, 
      name TEXT NOT NULL, 
      sex TEXT NOT NULL, 
      email TEXT NOT NULL, 
      phone TEXT NOT NULL)''')
    conn.commit()
    conn.close()
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, username, password) VALUES (?, ?, ?)", (name, username, password))
        conn.commit()
        conn.close()
        
        return redirect('/login')
    
    return render_template('signup.html')
        
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            #name = user[1]
            return redirect('/index')
            #return f'Welcome, {name}!'
        else:
            return 'Invalid username or password'
    
    return render_template('login.html')

    
@app.route('/wedding', methods =['POST','GET'])
def wedding():
    if request.method == 'POST':
           city = request.form['city']
           name = request.form['name']
           sex = request.form['gender']
           email = request.form['email']
           phone = request.form['phone']
        
           conn = sqlite3.connect('couples.db')
           cursor = conn.cursor()
           cursor.execute("INSERT INTO couple (city,name,sex,email,phone) VALUES (?,?,?,?,?)",(city,name,sex,email,phone) )
           conn.commit()
           conn.close()
        
           return redirect('/wedding')
    
    return render_template('wedding.html')
    
@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('couples.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM couple')
    couples = cur.fetchall()
    conn.close()
    return render_template('dashboard.html', couples=couples)

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        id = request.form['couple_id']

        with sqlite3.connect("couples.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM couple WHERE id=?", (id,))
            couples = cur.fetchall()

            if couples:
               
                return render_template("search_results.html", couples=couples)
            else:
               
                flash("Couple ID not found")
                return redirect(url_for('search'))
    else:
        return render_template("search.html")



@app.route("/jsdemo")
def jsdemo():
    return render_template('jsdemo.html')
@app.route('/logout')
def logout():
    #session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    create_users_table()
    create_couples_table()
    app.run(debug=True)