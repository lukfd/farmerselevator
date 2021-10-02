from farmerselevator import application
from farmerselevator.src.helper import *
import farmerselevator.constants

import bcrypt

from flask import request

# parameters: username, password, elevator
@application.route('/signin-form', methods=['POST'])
def signin_form():
    isElevator = request.form.get('elevator')
    username = request.form['username']
    password = request.form['password']

    con = lite.connect(farmerselevator.constants.databasePath)
    cur = con.cursor()

    # if it is an Elevator logging in
    if isElevator == "on":
        cur.execute(f"SELECT username, elevator_id, password from elevators WHERE username='{username}';")
        session['elevator'] = True
    else:
        cur.execute(f"SELECT username, farmer_id, password from farmers WHERE username='{username}';")
        session['elevator'] = False
    
    result = cur.fetchone()
    cur.close()
    
    if result: # A non-empty result evaluates to True.
        # 1st parameter checks if plain text password matches 2nd parameter hash in database
        # if true, password hashes correctly
        if bcrypt.checkpw(password.encode('utf-8'), result[2]):
            # create new session
            session['username'] = username
            session['user_id'] = result[1]
            # redirect to css/main page
            return redirect("/home", code=302)
    # failed to login
    return '''
        <link rel="stylesheet" type="text/css" href="/static/css/main.css">
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
        <a href="/signup">Don't have an account yet? Sign Up</a>
        '''
            
    
# Parameters: email, username, password, elevator
@application.route('/signup-form', methods=['POST'])
def signup_form():
    if 'username' in session:
        closeSession()

    isElevator = request.form.get('elevator')
    email = request.form['email']
    username = request.form['username']
    password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
    toInsert = ('name', email, password, username, 1, "default.png")

    con = lite.connect(farmerselevator.constants.databasePath) 
    cur = con.cursor()

    try:
        if isElevator == "on":
            cur.execute("""INSERT INTO elevators
                            (name, email, password, username, status, profile_image) 
                            VALUES (?, ?, ?, ?, ?, ?);""", toInsert)
        else:
            cur.execute("""INSERT INTO farmers
                            (name, email, password, username, status, profile_image) 
                            VALUES (?, ?, ?, ?, ?, ?);""", toInsert)
        con.commit()
        cur.close()
        # redirect to sign in page
        return redirect("/signin", code=302)
    except lite.Error as error:
            return "Failed: "+str(error)
    finally:
        if (con):
            con.close()