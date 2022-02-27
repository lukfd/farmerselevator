from farmerselevator import application
from farmerselevator import mysql
from farmerselevator.src.helper import *
import farmerselevator.constants

from flask import render_template
from flask import escape


@application.route('/profile/<string:profileType>/<string:id>', methods=['GET'])
def profile(profileType,id):
    loggedin = False
    if 'username' in session:
        loggedin = True
    #connect to database
    cur = mysql.get_db().cursor()
    if profileType == 'elevator':
        cur.execute(f"SELECT username, primary_contact, phone, email, address, profile_image from elevators WHERE elevator_id=%s;", (id,))
        result = cur.fetchone()
        if not result:
            cur.close()
            return f'''
            <h1>Farmers & Elevators</h1>
            <nav>
                <h3>Account {escape(id)} not found</h3>
                <a href="/signup">create a new account</a>
                <a href="/">home</a>
            </nav>
            '''
        cur.close()
        return render_template('profile.html', loggedin=loggedin, username=result[0], profile_type = "elevator", name=result[1], phone=result[2], email=result[3], address=result[4], image=str(result[5]))
    elif profileType == 'farmer':
        cur.execute(f"SELECT username, name, lastname, email, profile_image from farmers WHERE farmer_id=%s;", (id,))
        result = cur.fetchone()
        result = ['' if x is None else x for x in result]
        if not result:
            cur.close()
            return f'''
            <h1>Farmers & Elevators</h1>
            <nav>
                <h3>Account {escape(id)} not found</h3>
                <a href="/signup">create a new account</a>
                <a href="/">home</a>
            </nav>
            '''
        cur.close()
        return render_template('profile.html', loggedin=loggedin, username=result[0], profile_type = "farmer", name=result[1]+' '+result[2], email=result[3], image=str(result[4]))