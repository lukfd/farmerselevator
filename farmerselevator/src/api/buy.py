from farmerselevator import application
from farmerselevator.src.helper import *

from flask import render_template

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
