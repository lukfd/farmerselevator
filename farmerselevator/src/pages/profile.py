from farmerselevator import application
from farmerselevator.src.helper import *
import farmerselevator.constants

from flask import render_template
from flask import escape


@application.route('/profile/<string:id>', methods=['GET'])
def profile(id):
    loggedin = False
    if 'username' in session:
        loggedin = True
    # select from the table
    con = lite.connect(farmerselevator.constants.databasePath) 
    cur = con.cursor()
    cur.execute(f"SELECT username, primary_contact, phone, email, address, profile_image from elevators WHERE elevator_id='{id}';")
    result = cur.fetchone()
    if not result:  # An empty result evaluates to False.
        cur.execute(f"SELECT username, name, lastname, email, profile_image from farmers WHERE farmer_id='{id}';")
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
        else:
            cur.close()
            return render_template('profile.html', loggedin=loggedin, username=result[0], profile_type = "farmer", name=result[1]+' '+result[2], email=result[3], image=str(result[4]))    
    else:
        cur.close()
        return render_template('profile.html', loggedin=loggedin, username=result[0], profile_type = "elevator", name=result[1], phone=result[2], email=result[3], address=result[4], image=str(result[5]))
