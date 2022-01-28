from farmerselevator_production import application
from farmerselevator_production.src.helper import *

from flask import render_template

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