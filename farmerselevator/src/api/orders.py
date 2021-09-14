from farmerselevator import application
from farmerselevator.src.helper import *

from flask import request

from random import randint

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