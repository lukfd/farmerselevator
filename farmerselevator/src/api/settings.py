from farmerselevator import application
from farmerselevator import mysql
from farmerselevator.src.helper import *
import farmerselevator.constants

from flask import render_template
from flask import request
from flask import send_from_directory
from flask import escape

import os

import bcrypt

@application.route('/change-profile-information', methods=['POST'])
def change_profile_information():
    if 'username' in session:
        user_id = session['user_id']

        # Two different pages for elevator or farmer
        if session["elevator"] == True:
            email = request.form.get('email')
            contact_person = request.form.get('contact_person')
            phone = request.form.get('phone')
            address = request.form.get('address')
            # change in DB
            cur = mysql.get_db().cursor()

            toUpdate=(email, contact_person, phone, address, user_id)
            print(toUpdate)
            #create the new profile into the database
            try:
                cur.execute(f"""UPDATE elevators 
                            SET email=?, primary_contact=?,
                            phone=?, address=?
                            WHERE elevator_id=?;""", toUpdate)
                cur.commit()
                cur.close()
                # reload page
                return redirect('/settings-elevator', code=302)
            except:
                #return "Failed: "+str(error)
                if (cur):
                    cur.close()
                return
            finally:
                if (cur):
                    cur.close()
        else: # farmer
            email = request.form.get('email')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            phone = request.form.get('phone')
            address = request.form.get('address')
            # change in DB
            cur = mysql.get_db().cursor()
            toUpdate=(email, first_name, last_name, phone, address, user_id,)
            try:
                cur.execute(f"""UPDATE farmers 
                                SET email=?, name=?,
                                lastname=?,
                                phone=?, address=?
                                WHERE farmer_id=?;""",toUpdate)
                cur.commit()
                cur.close()
                # reload page
                return redirect('/settings-farmer', code=302)                
            except:
                #return "Failed: "+str(error)
                if (cur):
                    cur.close()
                return
            finally:
                if (cur):
                    cur.close()
    else:
        return redirect("/", code=302)

@application.route('/change-profile-image', methods=['POST'])
def change_profile_image():
    if 'username' in session:
        user_id = session['user_id']
        # save image
        file = request.files['image']
        extension = file.filename.split('.')[1]
        image_name = str(user_id)+"."+extension
        path = os.path.join(application.config['UPLOAD_FOLDER'], image_name)
        file.save(path)

        if session["elevator"] == True:
            cur = mysql.get_db().cursor()
            try:
                cur.execute(f"""UPDATE elevators 
                                SET profile_image='{image_name}' 
                                WHERE elevator_id='{user_id}';""")
                cur.commit()
                cur.close()
                # reload page
                return redirect('/settings-farmer', code=302)                
            except:
                #return "Failed: "+str(error)
                if (cur):
                    cur.close()
                return
            finally:
                if (cur):
                    cur.close()
        else:
            cur = mysql.get_db().cursor()
            try:
                cur.execute(f"""UPDATE farmers 
                                SET profile_image='{image_name}' 
                                WHERE farmer_id='{user_id}';""")
                cur.commit()
                cur.close()
                # reload page
                return redirect('/settings-farmer', code=302)                
            except:
                #return "Failed: "+str(error)
                if (cur):
                    cur.close()
                return
            finally:
                if (cur):
                    cur.close()

@application.route('/get-profile-image/<file>')
def get_profile_image(file):
    return send_from_directory(application.config['UPLOAD_FOLDER'], file)

@application.route('/change-password', methods=['GET', 'POST', 'PULL'])
def change_password():
    if 'username' in session:
        user_id = session['user_id']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        flag = True
        if new_password != confirm_password:
            return render_template("/settings-farmer", data = [flag]) # this needs to show some error

        new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

        cur = mysql.get_db().cursor()
        # Two different pages for elevator or farmer
        #print(session['username'])
        try:
            if session["elevator"] == True:
                # change password in DB:
                cur.execute('''UPDATE elevators SET password = ? WHERE elevator_id = ?''', (new_password, user_id))
                cur.commit()
            else:
                cur.execute('''UPDATE farmers SET password = ? WHERE farmer_id = ?''', (new_password, user_id))
                cur.commit()
                # reload page
            return redirect('/settings-farmer', code=302)                
        except:
            #return "Failed: "+str(error)
            if (cur):
                cur.close()
            return
        finally:
            if (cur):
                cur.close()
    else:
        return redirect("/", code=302)

@application.route('/delete-account')
def delete_account():
    if 'username' in session:
        # delete account from DB
        cur = mysql.get_db().cursor()
        try:
            username = session["username"]
            if session["elevator"] == True:
                cur.execute(f"""DELETE FROM elevators
                                WHERE elevator_id ='{session['user_id']}';""")
            else:
                cur.execute(f"""DELETE FROM farmers
                                WHERE farmer_id ='{session['user_id']}';""")
            cur.commit()
            closeSession()
            return f'''
            <h1>Farmers & Elevators</h1>
            <nav>
                <h3>Account {escape(username)} deleted</h3>
                <a href="/signup">create a new account</a>
                <a href="/">home</a>
            </nav>
            '''
        except:
            #return "Failed: "+str(error)
            if (cur):
                cur.close()
            return
        finally:
            if (cur):
                cur.close()
    else:
        return redirect("/", code=302)