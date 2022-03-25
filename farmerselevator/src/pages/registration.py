from farmerselevator import application
from farmerselevator.src.helper import *

from flask import render_template, request

import os
import smtplib

@application.route('/signin')
def signin():
    if 'username' in session:
        closeSession()
    return render_template('login.html')

@application.route('/signup')
def signup():
    return render_template('signup.html')

@application.route('/signup-elevator')
def signupElevator():
    return render_template('signup-elevator.html')

@application.route('/signup-elevator-form', methods=['POST'])
def signupElevatorForm():
    comapnyName = request.form['companyName']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    email = request.form['email']
    message = f"Subject: SIGN UP NEW ELEVATOR\n\nSENT BY: {comapnyName}\n\nFirst Name: {firstName}\n\nLast Name: {lastName}\n\nEmail: {email}\n\n"

    serverSmtp = smtplib.SMTP("smtp.gmail.com", 587)
    serverSmtp.starttls()
    serverSmtp.login(os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_PASSWORD'))
    serverSmtp.sendmail(os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_ADDRESS'), message)
    return render_template('signup-elevator-response.html')