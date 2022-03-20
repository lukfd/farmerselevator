from farmerselevator import application
from farmerselevator.src.helper import *

import os
import smtplib

from flask import render_template
from flask import request

@application.route('/contact-us')
def contact_us():
    return render_template('contact-us.html')

@application.route('/contact-us-message', methods=['POST'])
def contact_us_message():
    title = request.form['title']
    email = request.form['email']
    message = request.form['message']
    message = f"Subject: {title}\n\nSENT FROM: {email}\n\n" + message

    serverSmtp = smtplib.SMTP("smtp.gmail.com", 587)
    serverSmtp.starttls()
    serverSmtp.login(os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_PASSWORD'))
    serverSmtp.sendmail(os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_ADDRESS'), message)
    return contact_us()