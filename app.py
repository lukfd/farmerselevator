
# IMPORTs
from flask import Flask, render_template, url_for, redirect, request, escape
from flask import session

import sqlite3 as lite
from random import randint

app = Flask(__name__)

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
        session.pop('user_id', None)
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
    session.pop('user_id', None)
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
        con = lite.connect('base.db') 
        cur = con.cursor()
        cur.execute(f"SELECT username, elevator_id from elevators WHERE username='{username}' AND password = '{password}';")
        result = cur.fetchone()
        if not result:  # An empty result evaluates to False.
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
            session['username'] = username
            session['elevator'] = True
            session['user_id'] = result[1]
            # redirect to main page
            return redirect("/home", code=302) 
    else:
        # check username and password in DB
        con = lite.connect('base.db') 
        cur = con.cursor()
        cur.execute(f"SELECT username, farmer_id from farmers WHERE username='{username}' AND password = '{password}';")
        result = cur.fetchone()
        if not result:  # An empty result evaluates to False.
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
            session['username'] = username
            session['elevator'] = False
            session['user_id'] = result[1]
            # redirect to main page
            return redirect("/home", code=302)

# Parameters: email, username, password, elevator
@app.route('/signup-form', methods=['POST'])
def signup_form():
    if 'username' in session:
        session.pop('username', None)
        session.pop('elevator', None)
        session.pop('user_id', None)

    isElevator = request.form.get('elevator')
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    toInsert = ('name', randint(0, 100000), email, password, username, 1,)

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
            return "Failed: "+str(error)
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
            return "Failed: "+str(error)
        finally:
            if (con):
                con.close()

@app.route('/settings-elevator')
def settings_elevator():
    # check if user is in session
    if 'username' in session:
        # Two different pages for elevator or farmer
        if session["elevator"] == True:
            try:
                con = lite.connect('base.db') 
                cur = con.cursor()
                cur.execute(f"""SELECT email, primary_contact, phone, address
                from elevators WHERE elevator_id='{session['user_id']}';""")
                result = cur.fetchone()
                result = ['' if x is None else x for x in result]
                cur.close()
                return render_template('settings-elevator.html', result=result)
            except lite.Error as error:
                return "Failed: "+str(error)
            finally:
                if (con):
                    con.close()
        else: # Farmer
            try:
                con = lite.connect('base.db') 
                cur = con.cursor()
                cur.execute(f"""SELECT email, name, lastname, phone, address
                from farmers WHERE farmer_id='{session['user_id']}';""")
                result = cur.fetchone()
                result = ['' if x is None else x for x in result]
                cur.close()
                return render_template('settings-farmer.html', result=result)
            except lite.Error as error:
                return "Failed: "+str(error)
            finally:
                if (con):
                    con.close()
    else:
        return redirect("/", code=302)

@app.route('/settings-farmer')
def settings_farmer():
    # check if user is in session
    if 'username' in session:
        # Two different pages for elevator or farmer
        if session["elevator"] == True:
            try:
                con = lite.connect('base.db') 
                cur = con.cursor()
                cur.execute(f"""SELECT email, primary_contact, phone, address
                from elevators WHERE elevator_id='{session['user_id']}';""")
                result = cur.fetchone()
                result = ['' if x is None else x for x in result]
                cur.close()
                return render_template('settings-elevator.html', result=result)
            except lite.Error as error:
                return "Failed: "+str(error)
            finally:
                if (con):
                    con.close()
        else: # Farmer
            try:
                con = lite.connect('base.db') 
                cur = con.cursor()
                cur.execute(f"""SELECT email, name, lastname, phone, address
                from farmers WHERE farmer_id='{session['user_id']}';""")
                result = cur.fetchone()
                result = ['' if x is None else x for x in result]
                cur.close()
                return render_template('settings-farmer.html', result=result)
            except lite.Error as error:
                return "Failed: "+str(error)
            finally:
                if (con):
                    con.close()
    else:
        return redirect("/", code=302)

@app.route('/change-profile-information', methods=['POST'])
def change_profile_information():
    if 'username' in session:
        user_id = session['user_id']

        # Two different pages for elevator or farmer
        if session["elevator"] == True:
            email = request.form['email']
            contact_person = request.form['contact_person']
            phone = request.form['phone']
            address = request.form['address']
            image = request.form['image']
            # change in DB
            con = lite.connect('base.db') 
            cur = con.cursor()
            #create the new profile into the database
            try:
                cur.execute(f"""UPDATE elevators 
                            SET email='{email}', primary_contact='{contact_person}'
                            phone='{phone}', address='{address}',
                            profile_image='{image}' 
                            WHERE elevator_id='{user_id}';""")
                con.commit()
                cur.close()
                # reload page
                return redirect('/settings-elevator.html', code=302)
            except lite.Error as error:
                return "Failed: "+str(error)
            finally:
                if (con):
                    con.close()
        else: # farmer
            email = request.form['email']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            phone = request.form['phone']
            address = request.form['address']
            image = request.form['image']
            # change in DB
            con = lite.connect('base.db') 
            cur = con.cursor()
            try:
                cur.execute(f"""UPDATE farmers 
                                SET email='{email}', name='{first_name}'
                                lastname='{last_name}',
                                phone='{phone}', address='{address}',
                                profile_image='{image}' 
                                WHERE farmer_id='{user_id}';""")
                # reload page
                return redirect('/settings-farmer.html', code=302)                
            except lite.Error as error:
                return "Failed: "+str(error)
            finally:
                if (con):
                    con.close()
    else:
        return redirect("/", code=302)

@app.route('/change-password', methods=['POST'])
def change_password():
    
    if 'username' in session:
        user_id = session['user_id']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        # Two different pages for elevator or farmer
        if session["elevator"] == True:
            # change password in DB
            con = lite.connect('base.db') 
            cur = con.cursor()
            try:
                cur.execute(f"""UPDATE elevators 
                                SET password='{new_password}' 
                                WHERE elevator_id='{user_id}' AND password='{old_password}';""")
                # reload page
                return redirect('/settings-farmer.html', code=302)                
            except lite.Error as error:
                return "Failed: "+str(error)
            finally:
                if (con):
                    con.close()
        else:
            # change password in DB
            con = lite.connect('base.db') 
            cur = con.cursor()
            try:
                cur.execute(f"""UPDATE farmers 
                                SET password='{new_password}' 
                                WHERE farmer_id='{user_id}' AND password='{old_password}';""")
                # reload page
                return redirect('/settings-farmer.html', code=302)                
            except lite.Error as error:
                return "Failed: "+str(error)
            finally:
                if (con):
                    con.close()
    else:
        return redirect("/", code=302)

@app.route('/delete-account')
def delete_account():
    if 'username' in session:
        # Two different pages for elevator or farmer
        if session["elevator"] == True:
            username = session["username"]
            # delete account from DB
            

            return f'''
            <h1>Farmers & Elevators</h1>
            <nav>
                <h3>Account {escape(username)} deleted</h3>
                <a href="/signup">create a new account</a>
                <a href="/">home</a>
            </nav>
            '''
        else:
            username = session["username"]
            # delete account from DB


            return f'''
            <h1>Farmers & Elevators</h1>
            <nav>
                <h3>Account {escape(username)} deleted</h3>
                <a href="/signup">create a new account</a>
                <a href="/">home</a>
            </nav>
            '''
    else:
        return redirect("/", code=302)

@app.route('/home')
def homepage():
    # check if user is in session
    if 'username' in session:
        # Two different pages for elevator or farmer
        if session["elevator"] == True:
            return render_template('home-elevator.html', username=session["username"], id=session["user_id"])
        else:
            # get list of elevators
            con = lite.connect('base.db') 
            cur = con.cursor()
            cur.execute(f"SELECT username from elevators;")
            elevators = cur.fetchone()
            if not elevators:
                elevators = []
            # render page
            cur.close()
            return render_template('home-farmer.html', username=session["username"], id=session["user_id"], elevators=elevators)
    else:
        return redirect("/", code=302)

@app.route('/profile/<string:id>', methods=['GET'])
def profile(id):
    # select from the table
    con = lite.connect('base.db') 
    cur = con.cursor()
    cur.execute(f"SELECT username from elevators WHERE elevator_id='{id}';")
    result = cur.fetchone()
    if not result:  # An empty result evaluates to False.
        cur.execute(f"SELECT username from farmers WHERE farmer_id='{id}';")
        result = cur.fetchone()
        if not result:
            cur.close()
            return f'''
            <h1>Farmers & Elevators</h1>
            <nav>
                <h3>Account {escape(id)} not found</h3>
                <a href="/signup">create a new account</a>
                <a href="/">home</a>
            </nav>
            '''
        else:
            cur.close()
            return render_template('profile.html', username=result[0], profile_type = "farmer")    
    else:
        cur.close()
        return render_template('profile.html', username=result[0], profile_type = "elevator")

@app.route('/shop/<string:name>', methods=['GET'])
def shop(name):
    # get list of elevators
    con = lite.connect('base.db') 
    cur = con.cursor()
    cur.execute(f"SELECT elevator_id from elevators WHERE username='{name}';")
    elevator_id = cur.fetchone()
    if not elevator_id:
        return f'''
            <h1>Farmers & Elevators</h1>
            <nav>
                <h3>Shop {escape(name)} not found</h3>
                <a href="/signup">create a new account</a>
                <a href="/">home</a>
            </nav>
            '''
    # render page
    cur.close()
    return render_template('shop.html', username=name, id=elevator_id[0])

@app.route('/manage-shop')
def manage_shop():
    if 'username' in session:
        # Two different pages for elevator or farmer
        if session["elevator"] == True:
            return render_template('manage-shop.html', username=session['username'])
    else:
        return redirect("/home", code=302)

# this does not work
with app.test_request_context():
    url_for('static', filename='index.js')
