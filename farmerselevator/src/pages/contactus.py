from farmerselevator import application
from farmerselevator import mysql
from farmerselevator.src.helper import *
import farmerselevator.constants

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

    # also date and id

    toInsert = (title, email, message)

    cur = mysql.get_db().cursor()

    try:
        cur.execute("""INSERT INTO contact_us_messages
                        (message_title, sender_email, message_text, date) 
                        VALUES (%s, %s, %s, datetime('now', 'localtime'));""", toInsert)
        cur.close()
    except:
        return 'Server Error', 500
    finally:
        if (cur):
            cur.close()
    return contact_us()