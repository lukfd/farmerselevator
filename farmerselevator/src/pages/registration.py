from farmerselevator import application
from farmerselevator.src.helper import *

from flask import render_template

@application.route('/signin')
def signin():
    if 'username' in session:
        closeSession()
    return render_template('login.html')

@application.route('/signup')
def signup():
    return render_template('signup.html')