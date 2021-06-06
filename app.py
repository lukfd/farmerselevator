
# IMPORTs
from flask import Flask, render_template, url_for, redirect, request
from flask import session

import pymongo
import os
from pymongo import MongoClient
from random import randint
import json
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
# mongodb code
print(os.environ.get("USER"))
cluster = MongoClient(f'mongodb+srv://{os.environ.get("USER")}:{os.environ.get("PASSWORD")}@cluster0.ymdax.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["FarmersElevator"]




# CONSTANTS
app.secret_key = b'b[\x0e\x8c\x87\xdb\xa17\x9a\x8d\xdeO\r\xba|\xcd'

# WEBSITE

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin')
def signin():
    if 'username' in session:
        session.pop('username', None)
        session.pop('elevator', None)
    return '''
    <h1>Farmers & Elevators</h1>
    <form action="/signin-form" method="post">
        <label>Username:</label>
        <input type="text" name="username"/>
        <label>Password:</label>
        <input type="password" name="password"/>
        <label>elevator?</label>
        <input type="checkbox" name="elevator"/>
        <button type="submit">sign-in</button>
    </form>
    '''

@app.route('/signup')
def signup():
    return '''
    <h1>Farmers & Elevators</h1>
    <form action="/signup-form" method="post">
        <label>Email:</label>
        <input type="email" name="email"/>
        <label>Username:</label>
        <input type="text" name="username"/>
        <label>Password:</label>
        <input type="password" name="password"/>
        <label>retype Password:</label>
        <input type="password"/>
        <label>elevator?</label>
        <input type="checkbox" name="elevator"/>
        <button type="submit">sign-up</button>
    </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('elevator', None)
    return redirect("/", code=302) 

# parameters: username, password, elevator
@app.route('/signin-form', methods=['POST'])
def signin_form():
    isElevator = request.form.get('elevator')
    username = request.form['username']
    password = request.form['password']
    
    # if it is an Elevator logging in
    if isElevator == "on":
        # check username and password in DB           
        collection = db["Elevators"]
        if collection.find_one({"name": username, "password": password}):
            # create new session
            session['username'] = username
            session['elevator'] = True
            # redirect to main page
            return redirect("/home", code=302)
        else:
            # redirect to main page
            return '''
                 <h1>Farmers & Elevators</h1>
                 <h3>Login Failed, try again</h3>
                 <form action="/signin-form" method="post">
                     <label>Username:</label>
                     <input type="text" name="username"/>
                     <label>Password:</label>
                     <input type="password" name="password"/>
                     <label>elevator?</label>
                     <input type="checkbox" name="elevator"/>
                     <button type="submit">sign-in</button>
                 </form>
                 '''
    else:
        collection = db["Farmers"]
        if collection.find_one({"name": username, "password": password}):
            # create new session
            session['username'] = username
            session['elevator'] = True
            # redirect to main page
            return redirect("/home", code=302)
        else:
            return '''
                 <h1>Farmers & Elevators</h1>
                 <h3>Login Failed, try again</h3>
                 <form action="/signin-form" method="post">
                     <label>Username:</label>
                     <input type="text" name="username"/>
                     <label>Password:</label>
                     <input type="password" name="password"/>
                     <label>elevator?</label>
                     <input type="checkbox" name="elevator"/>
                     <button type="submit">sign-in</button>
                 </form>
                 '''


# Parameters: email, username, password, elevator
@app.route('/signup-form', methods=['POST'])
def signup_form():
    isElevator = request.form.get('elevator')
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']

    if(isElevator == "on"):
        #create the new profile into the database
        try:
            collection = db["Elevators"]
            collection.insert_one({"name": username, "email": email, "password": password, 
                                    "primary contact": None, "phone": None, "website": None, 
                                    "shop_url": None, "address": None,  "profile_img": None,"status": 1})
            # redirect to sign in page
            return redirect("/signin", code=302)
        except ConnectionFailure:
            print("Server is not available")
    else:
        # create the new profile into the database
        try:
            collection = db["Farmers"]
            collection.insert_one({"lastname": None, "name": username, "email:": email, 
                                    "password": password, "phone": None, "address": None, 
                                    "profile_img": None, "status": 1})
            # redirect to sign in page
            return redirect("/signin", code=302)
        except ConnectionFailure:
            print("Server is not available")


@app.route('/home')
def homepage():
    # check if user is in session
    if 'username' in session:
        # Two different pages for elevator or farmer
        if session["elevator"] == True:
            return f'''
            <h1>Farmers & Elevators</h1>
            <h3>Elevator {session["username"]} HomePage </h3><a href="/logout">logout</a>
            '''
        else:
            return f'''
            <h1>Farmers & Elevators</h1>
            <h3>Farmers's {session["username"]} HomePage </h3><a href="/logout">logout</a>
            '''
    else:
        return redirect("/", code=302)

# this does not work
with app.test_request_context():
    url_for('static', filename='index.js')
