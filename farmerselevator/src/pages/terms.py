from farmerselevator import application

from flask import render_template

@application.route('/terms')
def terms():
    return render_template('terms.html')