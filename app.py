from flask import Flask, render_template, url_for, redirect, request
import sqlite3 as lite
import pymongo
from pymongo import MongoClient
from random import randint
import json
from bson import json_util

app = Flask(__name__)
# mongodb code
cluster = MongoClient("mongodb+srv://farmer:tiger22@cluster0.ymdax.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = cluster["FarmersElevator"]




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin')
def signin():
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
    else:
        collection = db["Farmers"]
        if collection.find_one({"name": username, "password": password}):
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
    return '''
    <h1>Farmers & Elevators</h1>
    <h3>Homepage</h3>
    '''

# this does not work
with app.test_request_context():
    url_for('static', filename='index.js')
