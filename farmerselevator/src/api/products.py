from farmerselevator import application
from farmerselevator import mysql
from farmerselevator.src.helper import *
import farmerselevator.constants

from flask import request

@application.route('/add-product', methods=['POST'])
def add_product():
    if 'username' in session:
        if session['elevator'] is True:
            #elevator_id = request.form.get('elevator_id')
            elevator_id = session['user_id']
            product_name = request.form.get('product_name')
            #product_id = request.form.get('product_id')
            quantity_available = request.form.get('quantity_available')
            measure = request.form.get('measure')
            price = request.form.get('price')
            description = request.form.get('description')

            toInsert = (elevator_id, product_name, quantity_available, measure, price, description,)
            # inserting new product
            cur = mysql.get_db().cursor()
            try:
                cur.execute("""INSERT INTO products
                        (elevator_id, name, quantity_available, measure, price, description) 
                        VALUES (?, ?, ?, ?, ?, ?);""", toInsert)
                cur.commit()
                cur.close()
                # redirect to sign in page
                return redirect("/manage-shop", code=302)
            except:
                #return "Failed: "+str(error)
                if (cur):
                    cur.close()
                return
            finally:
                if (cur):
                    cur.close()
    else:
        return "not authorized"

@application.route('/update-product', methods=['POST'])
def update_product():
    if 'username' in session:
        if session['elevator'] is True:
            #elevator_id = request.form.get('elevator_id')
            elevator_id = session['user_id']
            product_name = request.form.get('product_name')
            product_id = request.form.get('product_id')
            quantity_available = request.form.get('quantity_available')
            measure = request.form.get('measure')
            price = request.form.get('price')
            description = request.form.get('description')
            #print(product_id)
            if product_id == '':
                return "you have to select a product id! <a href='/manage-shop'>Go back</a>"
            # if any of the form are empty, use old values
            olderValues = getProductInformation(product_id, elevator_id)
            # make the variables
            toUpdate = (elevator_id, product_name, product_id, quantity_available, measure, price, description,)
            toUpdate = substituteWithOlderValues(toUpdate, olderValues)
            # switching values
            toUpdate = (toUpdate[1], toUpdate[3], toUpdate[4], toUpdate[5], toUpdate[6], toUpdate[2], toUpdate[0],)
            # inserting new product
            cur = mysql.get_db().cursor()
            try:
                cur.execute("""UPDATE products
                        SET name=?, quantity_available=?, measure=?, price=?, description=? 
                        WHERE product_id=? AND elevator_id=?;""", toUpdate)
                cur.commit()
                cur.close()
                # redirect to sign in page
                return redirect("/manage-shop", code=302)
            except:
                #return "Failed: "+str(error)
                if (cur):
                    cur.close()
                return
            finally:
                if (cur):
                    cur.close()
    else:
        return "not authorized"

@application.route('/delete-product/<int:elevator_id>/<int:product_id>', methods=['GET','POST'])
def delete_product(elevator_id, product_id):
    if 'username' in session:
        if session['elevator'] == True:
            return deleteProduct(elevator_id, product_id)
    return "Not logged in"