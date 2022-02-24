from farmerselevator import application
from farmerselevator import mysql
from farmerselevator.src.helper import *
import farmerselevator.constants

from flask import request, jsonify

# Check if username is in a table
# 
# NOTES: print(request.form[0].to_dict(flat=False))
#
# @parameters: fromUserId, isElevator, toUser
# @return: True was found, False otherwise
@application.route('/isChat', methods=['POST'])
def isChat():

    request_data = request.get_json()

    fromUserId = request_data['fromUserId']
    isElevator = convertIsElevator(request_data['isElevator'])
    toUserId = getUserId(request_data['toUser'], not isElevator)

    cur = mysql.get_db().cursor()
    
    if isElevator:
        elevator_id = fromUserId
        farmer_id = toUserId
    else:
        farmer_id = fromUserId
        elevator_id = toUserId

    cur.execute("SELECT EXISTS(SELECT 1 FROM chats WHERE farmer_id=%s AND elevator_id=%s);", (farmer_id, elevator_id,))

    if cur.fetchone()[0] == 1:
        toReturn = {"return": "True"}
    else:
        toReturn = {"return": "False"}
    cur.close()


    return jsonify(toReturn)

# Check if a room is in a table 
# @parameters: fromUserId, isElevator, toUser
# @return: roomid if was found, 0 otherwise
@application.route('/getRoom', methods=['POST'])
def getRoom():

    request_data = request.get_json()

    fromUserId = request_data['fromUserId']
    isElevator = convertIsElevator(request_data['isElevator'])
    toUserId = getUserId(request_data['toUser'], not isElevator)

    cur = mysql.get_db().cursor()

    if isElevator:
        elevator_id = fromUserId
        farmer_id = toUserId
    else:
        farmer_id = fromUserId
        elevator_id = toUserId

    cur.execute("SELECT room_id FROM chats WHERE farmer_id = %s AND elevator_id = %s;", (farmer_id, elevator_id,))
    toReturn = cur.fetchone()
    cur.close()
    if toReturn is None:
        return jsonify({"return":"0"})
    else:
        return jsonify({"return": str(toReturn[0])})

# Select old messages from a selected room
# @parameter: room id
# @return: json with the messages
@application.route('/getPreviousMessages', methods=['POST'])
def getPreviousMessages():

    request_data = request.get_json()

    room = request_data['room']

    cur = mysql.get_db().cursor()

    cur.execute("SELECT messages FROM chats WHERE room_id = %s;", (room,))
    toReturn = cur.fetchone()
    cur.close()
    if (toReturn is None) or (toReturn[0] is None):
        return jsonify({"messages":""})
    else:
        return jsonify({"messages": str(toReturn[0])})

# @parameters: fromUserId and isElevator
# @return: an array of json with room and toUser info.
@application.route('/loadRooms', methods=['POST'])
def loadRooms():

    request_data = request.get_json()

    fromUserId = request_data['fromUserId']
    isElevator = convertIsElevator(request_data['isElevator'])

    cur = mysql.get_db().cursor()

    if isElevator:
        to = "farmer_id"
        fromUser = "elevator_id = %s"
    else:
        to = "elevator_id"
        fromUser = "farmer_id = %s"

    cur.execute("SELECT room_id , " + to + " FROM chats WHERE " + fromUser +";", (fromUserId,))
    result = cur.fetchall()
    cur.close()

    if result is None:
        return result
    else:
        toReturn = []
        for tuple in result:
            toReturn.append({"room": tuple[0], "toUser": getUsername(tuple[1], not isElevator)})
        return jsonify(toReturn)