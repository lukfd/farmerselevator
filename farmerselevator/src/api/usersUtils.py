from farmerselevator import application
from farmerselevator.src.helper import *
import farmerselevator.constants

from flask import request

##
##  DEPRECATED! NOT TESTED!
##

# Check if username is in a table
# @return: True was found, False otherwise
@application.route('/userExists', methods=['POST'])
def checkUserExistance():
    username = request.form.get('username')
    if request.form.get('isElevator') == 'True':
        isElevator = True
    elif request.form.get('isElevator') == 'False':
        isElevator = False
    else:
        return 'error'

    con = lite.connect(farmerselevator.constants.databasePath) 
    cur = con.cursor()
    tableName = 'farmers'
    if isElevator:
        tableName = 'elevators'
    cur.execute("SELECT EXISTS(SELECT 1 FROM " + tableName +" WHERE username=?);",(username,))
    if cur.fetchall() == 1:
        toReturn = 'True'
    else:
        toReturn = 'False'
    cur.close()
    return toReturn

# Get user_id
# @return int or null
@application.route('/getUserId', methods=['POST'])
def getUserId():
    username = request.form.get('username')

    if request.form.get('isElevator') == 'True':
        isElevator = True
    elif request.form.get('isElevator') == 'False':
        isElevator = False
    else:
        return 'error'
    
    con = lite.connect(farmerselevator.constants.databasePath) 
    cur = con.cursor()
    tableName = 'farmers'
    user_id = 'farmer_id'
    if isElevator:
        tableName = 'elevators'
        user_id = 'elevator_id'
    cur.execute("SELECT " + user_id + " FROM " + tableName + " WHERE username=?;",(username,))
    result = cur.fetchall()
    cur.close()
    return str(result)