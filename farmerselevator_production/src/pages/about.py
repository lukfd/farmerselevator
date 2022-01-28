from farmerselevator_production import application

from flask import render_template

@application.route('/about')
def about():
    return render_template('about.html')