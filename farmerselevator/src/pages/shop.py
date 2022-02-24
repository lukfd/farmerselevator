from farmerselevator import application
from farmerselevator import mysql
from farmerselevator.src.helper import *
import farmerselevator.constants

from flask import render_template
from flask import escape
from flask import request

@application.route('/shop', methods=['GET'])
def shop():
    name = request.args.get('name')
    if 'username' in session:
        # get list of elevators
        cur = mysql.get_db().cursor()
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
        cur = mysql.get_db().cursor()
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
