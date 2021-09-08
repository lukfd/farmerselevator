#    Written by Luca Comba and Daniel Taufiq
#    started September 2021

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

from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import request
from flask import escape

from random import randint

import sqlite3 as lite

from helper import *

###############################################
# MAIN

class Website:

    app = Flask(__name__)

    def __init__(self, app):
        self.app = app

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/contact-us')
    def contact_us():
        return render_template('contact-us.html')

    @app.route('/signin')
    def signin():
        if 'username' in session:
            closeSession()
        return '''
        <link rel="stylesheet" type="text/css" href="/static/css/main.css">
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
        <a href="/signup">Don't have an account yet? Sign Up</a>
        '''

    @app.route('/signup')
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

    @app.route('/logout')
    def logout():
        # remove the username from the session if it's there
        closeSession()
        return redirect("/", code=302)

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
        
    @app.route('/get-profile-image/<file>')
    def get_profile_image(self, file):
        return send_from_directory(self.app.config['UPLOAD_FOLDER'], file)

    @app.route('/home')
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
                # get list of orders
                orders = farmerGetOrders(session["user_id"])

                return render_template('home-farmer.html', username=session["username"], id=session["user_id"], elevators=elevators, orders=orders)
        else:
            return redirect("/", code=302)

    @app.route('/shop', methods=['GET'])
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

    @app.route('/buy/<int:product_id>/<int:elevator_id>', methods=['GET', 'POST'])
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

    @app.route('/submit-order/<int:product_id>/<int:elevator_id>/<int:farmer_id>', methods=['GET', 'POST'])
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

    @app.route('/manage-shop')
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

    @app.errorhandler(404)
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