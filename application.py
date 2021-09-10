#    Written by Luca Comba and Daniel Taufiq
#    started May 2021

###############################################
#  This is the server for the website         #
#                                             #
#  It uses flask, sqlite and our written      #
#  helper methods.                            #
#                                             #
#  for more infromation visit:                #
#  https://github.com/lukfd/farmerselevator   #
###############################################

###############################################
# IMPORTS
import os
from flask import Flask, render_template, url_for, redirect, request, escape, send_from_directory, session, jsonify, json
import bcrypt
import sqlite3 as lite
from random import randint

# OUR CODE from ./helper.py
from helper import *

# Flask name server
application = Flask(__name__)

# CONSTANTS
application.secret_key = b'b[\x0e\x8c\x87\xdb\xa17\x9a\x8d\xdeO\r\xba|\xcd'
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

##################################################
#                                                #
#  METHODS LIST and ports of the API:            #
#                                                #
#  # # # # # # # # # # # # # # # # # # # # # # # #  
#  
#  index():
#  contact_us():
#  contact_us_message():
#  signin():
#  signup():
#  logout():
#  signin_form():
#  signup_form():
#
#  settings_elevator():
#  settings_farmer():
#  change_profile_information():
#  change_profile_image():
#  get_profile_image(file):
#  change_password():
#  delete_account():
#  homepage():
#  getElevatorList():
#  profile(id):
#  shop():
#  buy(product_id, elevator_id)
#  submit_order(product_id, product_id)
#  mark_completed():
#  manage_shop():
#  add_product():
#  update_product():
#  delete_product(elevator_id, product_id)
#  page_not_found(e):
#
#####################################################

# WEBSITE MAIN FUNCTIONS

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/contact-us')
def contact_us():
    return render_template('contact-us.html')

@application.route('/contact-us-message', methods=['POST'])
def contact_us_message():
    title = request.form['title']
    email = request.form['email']
    message = request.form['message']

    # also date and id

    toInsert = (title, email, message)

    con = lite.connect('base.db') 
    cur = con.cursor()

    try:
        cur.execute("""INSERT INTO contact_us_messages
                        (message_title, sender_email, message_text, date) 
                        VALUES (?, ?, ?, datetime('now', 'localtime'));""", toInsert)
        con.commit()
        cur.close()
    except lite.Error as error:
            return "Failed: "+str(error)
    finally:
        if (con):
            con.close()
    return contact_us()

@application.route('/signin')
def signin():
    if 'username' in session:
        closeSession()
    return '''
    <link rel="stylesheet" type="text/css" href="/static/css/main.css">
    <link rel="stylesheet" type="text/css" href="/static/css/internal.css">
    <div class="header">
        <h1>Farmers & Elevators</h1>
    </div>
    <div class="page">
        <form action="/signin-form" method="post">
            <label>Username:</label>
            <input type="text" name="username"/>
            <label>Password:</label>
            <input type="password" name="password"/>
            <label>elevator?</label>
            <input type="checkbox" name="elevator"/>
            <button type="submit" class="button">Singin</button>
        </form>
        </div>
            <a href="/signup">Don't have an account yet? Sign Up</a>
        <div>
    </div>    
    '''

@application.route('/signup')
def signup():
    return '''
    <link rel="stylesheet" type="text/css" href="/static/css/main.css">
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
    <a href="/signin">Already have an account? Sign in</a>
    '''

@application.route('/logout')
def logout():
    # remove the username from the session if it's there
    closeSession()
    return redirect("/", code=302) 

# parameters: username, password, elevator
@application.route('/signin-form', methods=['POST'])
def signin_form():
    isElevator = request.form.get('elevator')
    username = request.form['username']
    password = request.form['password']

    con = lite.connect('base.db') 
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
    toInsert = ('name', randint(0, 100000), email, password, username, 1, "default.png")

    con = lite.connect('base.db') 
    cur = con.cursor()

    try:
        if isElevator == "on":
            cur.execute("""INSERT INTO elevators
                            (name, elevator_id, email, password, username, status, profile_image) 
                            VALUES (?, ?, ?, ?, ?, ?, ?);""", toInsert)
        else:
            cur.execute("""INSERT INTO farmers
                            (name, farmer_id, email, password, username, status, profile_image) 
                            VALUES (?, ?, ?, ?, ?, ?, ?);""", toInsert)
        con.commit()
        cur.close()
        # redirect to sign in page
        return redirect("/signin", code=302)
    except lite.Error as error:
            return "Failed: "+str(error)
    finally:
        if (con):
            con.close()


@application.route('/settings-elevator')
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

@application.route('/settings-farmer')
def settings_farmer():
    # check if user is in session
    if 'username' in session:
        # Two different pages for elevator or farmer
        if session["elevator"] == True:
            try:
                con = lite.connect('base.db') 
                cur = con.cursor()
                cur.execute(f"""SELECT email, primary_contact, phone, address, profile_image
                from elevators WHERE elevator_id='{session['user_id']}';""")
                result = cur.fetchone()
                result = ['' if x is None else x for x in result]
                cur.close()
                return render_template('settings-elevator.html', username=session['username'], result=result)
            except lite.Error as error:
                return "Failed: "+str(error)
            finally:
                if (con):
                    con.close()
        else: # Farmer
            try:
                con = lite.connect('base.db') 
                cur = con.cursor()
                cur.execute(f"""SELECT email, name, lastname, phone, address, profile_image
                from farmers WHERE farmer_id='{session['user_id']}';""")
                result = cur.fetchone()
                result = ['' if x is None else x for x in result]
                cur.close()
                return render_template('settings-farmer.html', username=session['username'], result=result)
            except lite.Error as error:
                return "Failed: "+str(error)
            finally:
                if (con):
                    con.close()
    else:
        return redirect("/", code=302)

@application.route('/change-profile-information', methods=['POST'])
def change_profile_information():
    if 'username' in session:
        user_id = session['user_id']

        # Two different pages for elevator or farmer
        if session["elevator"] == True:
            email = request.form.get('email')
            contact_person = request.form.get('contact_person')
            phone = request.form.get('phone')
            address = request.form.get('address')
            # change in DB
            con = lite.connect('base.db') 
            cur = con.cursor()
            #create the new profile into the database
            try:
                cur.execute(f"""UPDATE elevators 
                            SET email='{email}', primary_contact='{contact_person}',
                            phone='{phone}', address='{address}',
                            profile_image='{user_id}' 
                            WHERE elevator_id='{user_id}';""")
                con.commit()
                cur.close()
                # reload page
                return redirect('/settings-elevator', code=302)
            except lite.Error as error:
                return "Failed: "+str(error)
            finally:
                if (con):
                    con.close()
        else: # farmer
            email = request.form.get('email')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            phone = request.form.get('phone')
            address = request.form.get('address')
            # change in DB
            con = lite.connect('base.db') 
            cur = con.cursor()
            try:
                cur.execute(f"""UPDATE farmers 
                                SET email='{email}', name='{first_name}',
                                lastname='{last_name}',
                                phone='{phone}', address='{address}',
                                profile_image='{user_id}' 
                                WHERE farmer_id='{user_id}';""")
                con.commit()
                cur.close()
                # reload page
                return redirect('/settings-farmer', code=302)                
            except lite.Error as error:
                return "Failed: "+str(error)
            finally:
                if (con):
                    con.close()
    else:
        return redirect("/", code=302)

@application.route('/change-profile-image', methods=['POST'])
def change_profile_image():
    if 'username' in session:
        user_id = session['user_id']
        # save image
        file = request.files['image']
        extension = file.filename.split('.')[1]
        image_name = str(user_id)+"."+extension
        path = os.path.join(application.config['UPLOAD_FOLDER'], image_name)
        file.save(path)

        if session["elevator"] == True:
            con = lite.connect('base.db') 
            cur = con.cursor()
            try:
                cur.execute(f"""UPDATE elevators 
                                SET profile_image='{image_name}' 
                                WHERE elevator_id='{user_id}';""")
                con.commit()
                cur.close()
                # reload page
                return redirect('/settings-farmer', code=302)                
            except lite.Error as error:
                return "Failed: "+str(error)
            finally:
                if (con):
                    con.close()
        else:
            con = lite.connect('base.db') 
            cur = con.cursor()
            try:
                cur.execute(f"""UPDATE farmers 
                                SET profile_image='{image_name}' 
                                WHERE farmer_id='{user_id}';""")
                con.commit()
                cur.close()
                # reload page
                return redirect('/settings-farmer', code=302)                
            except lite.Error as error:
                return "Failed: "+str(error)
            finally:
                if (con):
                    con.close()

@application.route('/get-profile-image/<file>')
def get_profile_image(file):
    return send_from_directory(application.config['UPLOAD_FOLDER'], file)

@application.route('/change-password', methods=['GET', 'POST', 'PULL'])
def change_password():
    if 'username' in session:
        user_id = session['user_id']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        flag = True
        if new_password != confirm_password:
            return render_template("/settings-farmer", data = [flag]) # this needs to show some error

        new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

        con = lite.connect('base.db') 
        cur = con.cursor()
        # Two different pages for elevator or farmer
        #print(session['username'])
        try:
            if session["elevator"] == True:
                # change password in DB:
                cur.execute('''UPDATE elevators SET password = ? WHERE elevator_id = ?''', (new_password, user_id))
                con.commit()
            else:
                cur.execute('''UPDATE farmers SET password = ? WHERE farmer_id = ?''', (new_password, user_id))
                con.commit()
                # reload page
            return redirect('/settings-farmer', code=302)                
        except lite.Error as error:
            return "Failed: "+str(error)
        finally:
            if (con):
                con.close()
    else:
        return redirect("/", code=302)

@application.route('/delete-account')
def delete_account():
    if 'username' in session:
        # delete account from DB
        con = lite.connect('base.db') 
        cur = con.cursor()
        try:
            username = session["username"]
            if session["elevator"] == True:
                cur.execute(f"""DELETE FROM elevators
                                WHERE elevator_id ='{session['user_id']}';""")
            else:
                cur.execute(f"""DELETE FROM farmers
                                WHERE farmer_id ='{session['user_id']}';""")
            con.commit()
            closeSession()
            return f'''
            <h1>Farmers & Elevators</h1>
            <nav>
                <h3>Account {escape(username)} deleted</h3>
                <a href="/signup">create a new account</a>
                <a href="/">home</a>
            </nav>
            '''
        except lite.Error as error:
                return "Failed: "+str(error)
        finally:
            if (con):
                con.close()
    else:
        return redirect("/", code=302)

@application.route('/home')
def homepage():
    # check if user is in session
    if 'username' in session:
        # Two different pages for elevator or farmer
        if session["elevator"] == True:
            orders = elevatorGetOrders(session["user_id"])
            return render_template('home-elevator.html', username=session["username"], id=session["user_id"], orders=orders)
        else:
            # get list of elevators
            elevators = getElevatorArray()
            correctElevators = []
            for i in elevators:
                for tuple in i:
                    correctElevators.append(tuple)
            elevators = correctElevators
            # get list of orders
            orders = farmerGetOrders(session["user_id"])

            return render_template('home-farmer.html', username=session["username"], id=session["user_id"], elevators=elevators, orders=orders)
    else:
        return redirect("/", code=302)

@application.route('/getElevatorList', methods=['GET'])
def getElevatorList():
    # get names of elevators
    elevators = getElevatorArray()

    data = []
    for i in range(len(elevators)):
        data.append({"name": elevators[i][0]})

    # return json
    return jsonify(data)

@application.route('/profile/<string:id>', methods=['GET'])
def profile(id):
    loggedin = False
    if 'username' in session:
        loggedin = True
    # select from the table
    con = lite.connect('base.db') 
    cur = con.cursor()
    cur.execute(f"SELECT username, primary_contact, phone, email, address, profile_image from elevators WHERE elevator_id='{id}';")
    result = cur.fetchone()
    if not result:  # An empty result evaluates to False.
        cur.execute(f"SELECT username, name, lastname, email, profile_image from farmers WHERE farmer_id='{id}';")
        result = cur.fetchone()
        result = ['' if x is None else x for x in result]
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
            return render_template('profile.html', loggedin=loggedin, username=result[0], profile_type = "farmer", name=result[1]+' '+result[2], email=result[3], image=str(result[4]))    
    else:
        cur.close()
        return render_template('profile.html', loggedin=loggedin, username=result[0], profile_type = "elevator", name=result[1], phone=result[2], email=result[3], address=result[4], image=str(result[5]))

@application.route('/shop', methods=['GET'])
def shop():
    name = request.args.get('name')
    if 'username' in session:
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
        products = getProductList(elevator_id[0])
        return render_template('shop.html', username=name, id=elevator_id[0], loggedin=True, products=products)
    else:
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
        cur.close()
        # render page
        products = getProductList(elevator_id[0])
        return render_template('shop.html', username=name, id=elevator_id[0], loggedin=False, products=products)

@application.route('/buy/<int:product_id>/<int:elevator_id>', methods=['GET', 'POST'])
def buy(product_id, elevator_id):
    if 'username' in session:
        if session['elevator'] == False:
            farmer_id = session['user_id']
            # get information of product from product_id
            result = getProductInformation(product_id, elevator_id)
            #print(result)
            return render_template('buy.html', product_id=product_id,
                elevator_id=elevator_id, farmer_id=farmer_id, name=result[1],
                quantity_available=result[3], measure=result[4],
                price=result[5], description=result[6])
    # not signed in or not a Farmer account
    return """
    <link rel="stylesheet" type="text/css" href="/static/css/main.css">
    <h1>Farmers & Elevators</h1>
    <h3>To order any product you need to have a farmer account</h3>
    <a href="/signin">Sign In</a>
    <a href="/signup">Don't have an account yet? Sign Up</a>
    """

@application.route('/submit-order/<int:product_id>/<int:elevator_id>/<int:farmer_id>', methods=['GET', 'POST'])
def submit_order(product_id, elevator_id, farmer_id):
    if 'username' in session:
        if session['elevator'] == False:
            quantity_requested = request.form.get('quantity')
            measure = request.form.get('measure')
            description = request.form.get('description')
            order_id = randint(0, 100000)
            # get product name
            product_name = getProductName(elevator_id, product_id)
            product_name = product_name[0]
            # send info to orders table
            result = insertNewOrder(order_id, product_id, elevator_id, farmer_id, quantity_requested, measure, description, product_name)
            # send email informations
            # return message
            if result == True:
                return """
                <link rel="stylesheet" type="text/css" href="/static/css/main.css">
                <title>Order Sent!</title>
                <nav>
                    <a href="/home">home</a> |
                    <a href="/logout">logout</a> |
                    <a href="/settings-farmer">settings</a>
                </nav>
                <h1>The order has been sent successfully!</h1>
                """
            else:
                return "Error: the new order could not been send at this time"
    # not signed in or not a Farmer account
    return """
    <link rel="stylesheet" type="text/css" href="/static/css/main.css">
    <h1>Farmers & Elevators</h1>
    <h3>To order any product you need to have a farmer account</h3>
    <a href="/signin">Sign In</a>
    <a href="/signup">Don't have an account yet? Sign Up</a>
    """

@application.route('/mark-completed', methods=['GET'])
def mark_completed():
    if 'username' in session:
        product_id = request.args.get('product_id')
        elevator_id = request.args.get('elevator_id')
        order_id = request.args.get('order_id')
        return markAsComplete(product_id, elevator_id, order_id)
    else:
        return """
            <link rel="stylesheet" type="text/css" href="/static/css/main.css">
            you have to be logged in
            """

@application.route('/manage-shop')
def manage_shop():
    if 'username' in session:
        # Two different pages for elevator or farmer
        if session["elevator"] == True:
            id=session['user_id']
            # select from the table
            result = getProductList(id)
            return render_template('manage-shop.html', username=session['username'], products=result, user_id=id)
    else:
        return redirect("/home", code=302)

@application.route('/add-product', methods=['POST'])
def add_product():
    if 'username' in session:
        if session['elevator'] is True:
            #elevator_id = request.form.get('elevator_id')
            elevator_id = session['user_id']
            product_name = request.form.get('product_name')
            product_id = request.form.get('product_id')
            quantity_available = request.form.get('quantity_available')
            measure = request.form.get('measure')
            price = request.form.get('price')
            description = request.form.get('description')
            #print(product_id)
            if product_id is '':
                product_id = randint(0, 100000)
            toInsert = (elevator_id, product_name, product_id, quantity_available, measure, price, description,)
            # inserting new product
            con = lite.connect('base.db') 
            cur = con.cursor()
            try:
                cur.execute("""INSERT INTO products
                        (elevator_id, name, product_id, quantity_available, measure, price, description) 
                        VALUES (?, ?, ?, ?, ?, ?, ?);""", toInsert)
                con.commit()
                cur.close()
                # redirect to sign in page
                return redirect("/manage-shop", code=302)
            except lite.Error as error:
                    return "Failed: "+str(error)
            finally:
                if (con):
                    con.close()
    else:
        return "not authorized"

@application.route('/update-product', methods=['POST'])
def update_product():
    if 'username' in session:
        if session['elevator'] is True:
            #elevator_id = request.form.get('elevator_id')
            elevator_id = session['user_id']
            product_name = request.form.get('product_name')
            product_id = request.form.get('product_id')
            quantity_available = request.form.get('quantity_available')
            measure = request.form.get('measure')
            price = request.form.get('price')
            description = request.form.get('description')
            #print(product_id)
            if product_id is '':
                return "you have to select a product id! <a href='/manage-shop'>Go back</a>"
            # if any of the form are empty, use old values
            olderValues = getProductInformation(product_id, elevator_id)
            # make the variables
            toUpdate = (elevator_id, product_name, product_id, quantity_available, measure, price, description,)
            toUpdate = substituteWithOlderValues(toUpdate, olderValues)
            # switching values
            toUpdate = (toUpdate[1], toUpdate[3], toUpdate[4], toUpdate[5], toUpdate[6], toUpdate[2], toUpdate[0],)
            # inserting new product
            con = lite.connect('base.db') 
            cur = con.cursor()
            try:
                cur.execute("""UPDATE products
                        SET name=?, quantity_available=?, measure=?, price=?, description=? 
                        WHERE product_id=? AND elevator_id=?;""", toUpdate)
                con.commit()
                cur.close()
                # redirect to sign in page
                return redirect("/manage-shop", code=302)
            except lite.Error as error:
                    return "Failed: "+str(error)
            finally:
                if (con):
                    con.close()
    else:
        return "not authorized"

@application.route('/delete-product/<int:elevator_id>/<int:product_id>', methods=['GET','POST'])
def delete_product(elevator_id, product_id):
    if 'username' in session:
        if session['elevator'] == True:
            return deleteProduct(elevator_id, product_id)
    return "Not logged in"

@application.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return """
    <link rel="stylesheet" type="text/css" href="/static/css/main.css">
    <h1>Page not found...</h1>
    <nav>
        <a href="/home" type="button">Home</a>
        <a href="/signin" type="button">Sign In</a>
        <a href="/signup" type="button">Sign Up</a>
    </nav>
    """

if __name__ == '__main__':
    application.run()