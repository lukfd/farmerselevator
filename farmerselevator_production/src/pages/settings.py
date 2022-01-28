from farmerselevator_production import application
from farmerselevator_production.src.helper import *
import farmerselevator_production.constants

from flask import render_template

@application.route('/settings-elevator')
def settings_elevator():
    # check if user is in session
    if 'username' in session:
        # Two different pages for elevator or farmer
        if session["elevator"] == True:
            try:
                con = lite.connect(farmerselevator_production.constants.databasePath) 
                cur = con.cursor()
                cur.execute(f"""SELECT email, primary_contact, phone, address
                from elevators WHERE elevator_id='{session['user_id']}';""")
                result = cur.fetchone()
                result = ['' if x is None else x for x in result]
                cur.close()
                return render_template('settings-elevator.html', result=result)
            except lite.Error as error:
                return "Failed: "+str(error)
            finally:
                if (con):
                    con.close()
        else: # Farmer
            try:
                con = lite.connect(farmerselevator_production.constants.databasePath) 
                cur = con.cursor()
                cur.execute(f"""SELECT email, name, lastname, phone, address
                from farmers WHERE farmer_id='{session['user_id']}';""")
                result = cur.fetchone()
                result = ['' if x is None else x for x in result]
                cur.close()
                return render_template('settings-farmer.html', result=result)
            except lite.Error as error:
                return "Failed: "+str(error)
            finally:
                if (con):
                    con.close()
    else:
        return redirect("/", code=302)

@application.route('/settings-farmer')
def settings_farmer():
    # check if user is in session
    if 'username' in session:
        # Two different pages for elevator or farmer
        if session["elevator"] == True:
            try:
                con = lite.connect(farmerselevator_production.constants.databasePath) 
                cur = con.cursor()
                cur.execute(f"""SELECT email, primary_contact, phone, address, profile_image
                from elevators WHERE elevator_id='{session['user_id']}';""")
                result = cur.fetchone()
                result = ['' if x is None else x for x in result]
                cur.close()
                return render_template('settings-elevator.html', username=session['username'], result=result)
            except lite.Error as error:
                return "Failed: "+str(error)
            finally:
                if (con):
                    con.close()
        else: # Farmer
            try:
                con = lite.connect(farmerselevator_production.constants.databasePath) 
                cur = con.cursor()
                cur.execute(f"""SELECT email, name, lastname, phone, address, profile_image
                from farmers WHERE farmer_id='{session['user_id']}';""")
                result = cur.fetchone()
                result = ['' if x is None else x for x in result]
                cur.close()
                return render_template('settings-farmer.html', username=session['username'], result=result)
            except lite.Error as error:
                return "Failed: "+str(error)
            finally:
                if (con):
                    con.close()
    else:
        return redirect("/", code=302)