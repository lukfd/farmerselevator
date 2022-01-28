from farmerselevator_production import application
from farmerselevator_production.src.helper import *

from flask import render_template

@application.route('/signin')
def signin():
    if 'username' in session:
        closeSession()
    return render_template('login.html')

@application.route('/signup')
def signup():
    return render_template('signup.html')