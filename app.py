from flask import Flask, render_template, url_for, redirect, request
import sqlite3 as lite
from random import randint

app = Flask(__name__)

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
        con = lite.connect('base.db') 
        cur = con.cursor()
        cur.execute(f"SELECT username from elevators WHERE username='{username}' AND Password = '{password}';")
        if not cur.fetchone():  # An empty result evaluates to False.
            cur.close()
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
            # create new session

            # redirect to main page
            return redirect("/home", code=302) 
    else:
        # check username and password in DB
        con = lite.connect('base.db') 
        cur = con.cursor()
        cur.execute(f"SELECT username from farmers WHERE username='{username}' AND Password = '{password}';")
        if not cur.fetchone():  # An empty result evaluates to False.
            cur.close()
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
            # create new session
            
            # redirect to main page
            return redirect("/home", code=302)

# Parameters: email, username, password, elevator
@app.route('/signup-form', methods=['POST'])
def signup_form():
    isElevator = request.form.get('elevator')
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    toInsert = ('name', randint(0, 100000), email, password, username, 1,)
    print(len(toInsert))

    if isElevator == "on":
        con = lite.connect('base.db') 
        cur = con.cursor()
        #create the new profile into the database
        try:
            cur.execute("""INSERT INTO elevators
                            (name, elevator_id, email, password, username, status) 
                            VALUES (?, ?, ?, ?, ?, ?);""", toInsert)
            con.commit()
            cur.close()
            # redirect to sign in page
            return redirect("/signin", code=302)
        except lite.Error as error:
            return "Failed "+str(error)
        finally:
            if (con):
                con.close()
    else:
        con = lite.connect('base.db') 
        cur = con.cursor()
        # create the new profile into the database
        try:
            cur.execute("""INSERT INTO farmers
                            (name, farmer_id, email, password, username, status) 
                            VALUES (?, ?, ?, ?, ?, ?);""", toInsert)
            con.commit()
            cur.close()
            # redirect to sign in page
            return redirect("/signin", code=302)
        except lite.Error as error:
            return "Failed "+str(error)
        finally:
            if (con):
                con.close()

@app.route('/home')
def homepage():
    return '''
    <h1>Farmers & Elevators</h1>
    <h3>Homepage</h3>
    '''

# this does not work
with app.test_request_context():
    url_for('static', filename='index.js')
