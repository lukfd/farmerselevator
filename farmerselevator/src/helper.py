#    Written by Luca Comba and Daniel Taufiq
#    started May 2021

##########################################
#  In this file you will find helper     #
#  methods that are used in app.py       #
#  server.                               #
#                                        #
#  to use this module and its function   #
#  just                                  #
#                                        #
#  from helper import *                  #
##########################################

from flask import session, redirect
import sqlite3 as lite
import  farmerselevator.constants

#########################################################
#
#   All the HELPER METHODS that are present in this file:S
#
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #
#
#   closeSession():
#
#   getProductList(id):
#
#   getProductInformation(product_id, elevator_id):
#
#   getProductName(elevator_id, product_id):
#
#   deleteProduct(elevator_id, product_id):
#
#   insertNewOrder(order_id, product_id, elevator_id, farmer_id, quantity_requested, measure, description, product_name):
#
#   markAsComplete(product_id, elevator_id, order_id):
#
#   elevatorGetOrders(elevator_id):
#
#   farmerGetOrders(farmer_id):
#
#   substituteWithOlderValues(toUpdate, olderValues):
#
#   getElevatorArray():
#
##########################################################

def closeSession():
    session.pop('username', None)
    session.pop('elevator', None)
    session.pop('user_id', None)

def getProductList(id):
    con = lite.connect(farmerselevator.constants.databasePath) 
    cur = con.cursor()
    cur.execute(f"SELECT * from products WHERE elevator_id='{id}';")
    result = cur.fetchall()
    if not result:
        result = []
    else:
        result = ['' if x is None else x for x in result]
    cur.close()
    return result

def getProductInformation(product_id, elevator_id):
    con = lite.connect(farmerselevator.constants.databasePath) 
    cur = con.cursor()
    cur.execute(f"SELECT * from products WHERE elevator_id='{elevator_id}' AND product_id='{product_id}';")
    result = cur.fetchall()
    if not result:
        result = []
    else:
        result = ['' if x is None else x for x in result]
    cur.close()
    return result[0]

def getProductName(elevator_id, product_id):
    con = lite.connect(farmerselevator.constants.databasePath) 
    cur = con.cursor()
    cur.execute(f"SELECT name from products WHERE elevator_id='{elevator_id}' AND product_id='{product_id}';")
    result = cur.fetchall()
    if not result:
        result = []
    else:
        result = ['' if x is None else x for x in result]
    cur.close()
    return result[0]

def deleteProduct(elevator_id, product_id):
    toDelete = (elevator_id, product_id,)
    con = lite.connect(farmerselevator.constants.databasePath)
    cur = con.cursor()
    try:
        deletedProductToIntesert = getProductInformation(product_id, elevator_id)
        # deletedProductToInsert is a tuple (elevator_id, name, product_id, quantity_av, measure, price, description)
        cur.execute("""INSERT INTO deleted_products
                    (elevator_id, name, product_id, quantity_available, measure, price, description) 
                    VALUES (?, ?, ?, ?, ?, ?, ?);""", deletedProductToIntesert)
        con.commit()
        cur.execute("DELETE from products WHERE elevator_id=? AND product_id=?;", toDelete)
        con.commit()
        cur.close()
        # return success
        return redirect("/manage-shop", code=302)
    except lite.Error as error:
        return "Error:" + str(error)
    finally:
        if (con):
            con.close()

def insertNewOrder(product_id, elevator_id, farmer_id, quantity_requested, measure, description, product_name):
    # missing date, status, quantity_type, description, payment
    toInsert = (product_id, elevator_id, farmer_id, quantity_requested, measure, description, product_name)
    # inserting new product
    con = lite.connect(farmerselevator.constants.databasePath) 
    cur = con.cursor()
    try:
        cur.execute("""INSERT INTO orders
                (product_id, elevator_id, farmer_id, quantity_int, date, status, quantity_type, description, product_name) 
                VALUES (?, ?, ?, ?, datetime('now', 'localtime'), 'to process', ?, ?, ?);""", toInsert)
        con.commit()
        # UPDATE in products table quantity available
        cur.execute(f"SELECT quantity_available from products WHERE elevator_id='{elevator_id}' AND product_id='{product_id}';")
        quantity_available = cur.fetchall()
        toUpdate = (int(quantity_available[0][0]-int(quantity_requested)), elevator_id, product_id,)
        cur.execute(f"""UPDATE products 
                        SET quantity_available=? 
                        WHERE elevator_id=? AND product_id=?;""", toUpdate)
        con.commit()
        cur.close()
        # return success
        return True
    except lite.Error as error:
        print(error)
        return False
    finally:
        if (con):
            con.close()

def markAsComplete(product_id, elevator_id, order_id):
    # update orders table
    toUpdate = ('completed', elevator_id, product_id, order_id,)
    con = lite.connect(farmerselevator.constants.databasePath) 
    cur = con.cursor()
    try:
        cur.execute(f"""UPDATE orders 
                        SET status=?, completed_date=datetime('now', 'localtime')  
                        WHERE elevator_id=? AND product_id=? AND order_id=?;""", toUpdate)
        con.commit()
        cur.close()
        # return success
        return redirect("/home", code=302)
    except lite.Error as error:
        print(error)
        return "Could not mark as completed"
    finally:
        if (con):
            con.close()

def elevatorGetOrders(elevator_id):
    con = lite.connect(farmerselevator.constants.databasePath) 
    cur = con.cursor()
    cur.execute(f"SELECT * from orders WHERE elevator_id='{elevator_id}';")
    result = cur.fetchall()
    if not result:
        result = []
    else:
        result = ['' if x is None else x for x in result]
    cur.close()
    return result

def farmerGetOrders(farmer_id):
    con = lite.connect(farmerselevator.constants.databasePath) 
    cur = con.cursor()
    cur.execute(f"SELECT * from orders WHERE farmer_id='{farmer_id}';")
    result = cur.fetchall()
    if not result:
        result = []
    else:
        result = ['' if x is None else x for x in result]
    cur.close()
    return result

def substituteWithOlderValues(toUpdate, olderValues):
    newToUpdate = list(toUpdate)
    for i in range(0, len(toUpdate)):
        if toUpdate[i] == '':
            newToUpdate[i] = olderValues[i]
    return tuple(newToUpdate)

def getElevatorArray():
    # get list of elevators
    con = lite.connect(farmerselevator.constants.databasePath) 
    cur = con.cursor()
    cur.execute(f"SELECT username from elevators;")
    elevators = cur.fetchall()
    if not elevators:
        elevators = []
    # render page
    cur.close()
    # return elevators array
    return elevators

# @parameters: username is a string, and isElevator is a boolean.
# @return: the userid found, otherwise 0
def getUserId(username, isElevator):
    con = lite.connect(farmerselevator.constants.databasePath) 
    cur = con.cursor()
    tableName = 'farmers'
    user_id = 'farmer_id'
    if isElevator:
        tableName = 'elevators'
        user_id = 'elevator_id'
    cur.execute("SELECT " + user_id + " FROM " + tableName + " WHERE username=?;",(username,))
    result = cur.fetchone()
    cur.close()

    if result is None:
        return 0
    return str(result[0])

# @parameter: isElevator as string
# @return: boolean
def convertIsElevator(isElevator):
    if isElevator == 'True':
        return True
    elif isElevator == 'False':
        return False
    else:
        return 'error'

# @parameter:
# @return:
def getUsername(userId, isElevator):
    con = lite.connect(farmerselevator.constants.databasePath) 
    cur = con.cursor()
    tableName = 'farmers'
    key = 'farmer_id'
    if isElevator:
        tableName = 'elevators'
        key = 'elevator_id'
    cur.execute("SELECT username FROM " + tableName + " WHERE " + key + "=?;",(userId,))
    result = cur.fetchone()
    cur.close()

    if result is None:
        return 0
    return str(result[0])