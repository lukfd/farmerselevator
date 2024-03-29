from farmerselevator import application
from farmerselevator import mysql
from farmerselevator.src.helper import *
import farmerselevator.constants

from flask import request, jsonify

# Check if username is in a table
# @return: True was found, False otherwise
@application.route('/userExists', methods=['POST'])
def checkUserExistance():

    request_data = request.get_json()

    username = request_data['username']
    isElevator = convertIsElevator(request_data['isElevator'])

    cur = mysql.get_db().cursor()
    
    if isElevator:
        tableName = 'elevators'
    else:
        tableName = 'farmers'

    cur.execute("SELECT EXISTS(SELECT 1 FROM " + tableName +" WHERE username=%s);",(username,))

    if cur.fetchone()[0] == 1:
        toReturn = {"return": "True"}
    else:
        toReturn = {"return": "False"}
    cur.close()

    return jsonify(toReturn)

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
    
    cur = mysql.get_db().cursor()
    tableName = 'farmers'
    user_id = 'farmer_id'
    if isElevator:
        tableName = 'elevators'
        user_id = 'elevator_id'
    cur.execute("SELECT " + user_id + " FROM " + tableName + " WHERE username=%s;",(username,))
    result = cur.fetchall()
    cur.close()
    return str(result)