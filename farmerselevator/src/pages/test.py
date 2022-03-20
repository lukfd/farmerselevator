from farmerselevator import application

import os
import smtplib

from flask import render_template

@application.route('/test')
def test():

    message = "This was sent by Luca"
    serverSmtp = smtplib.SMTP("smtp.gmail.com", 587)
    serverSmtp.starttls()
    serverSmtp.login(os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_PASSWORD'))
    serverSmtp.sendmail(os.getenv('EMAIL_ADDRESS'), "luca.comba98@gmail.com", message)

    return render_template('test.html')