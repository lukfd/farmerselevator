from farmerselevator_production import application
from farmerselevator_production.src.helper import *
import farmerselevator_production.constants

from flask import render_template
from flask import request
import sqlite3 as lite

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

    con = lite.connect(farmerselevator_production.constants.databasePath) 
    cur = con.cursor()

    try:
        cur.execute("""INSERT INTO contact_us_messages
                        (message_title, sender_email, message_text, date) 
                        VALUES (?, ?, ?, datetime('now', 'localtime'));""", toInsert)
        con.commit()
        cur.close()
    except lite.Error as error:
            return "Failed: "+str(error)
    finally:
        if (con):
            con.close()
    return contact_us()