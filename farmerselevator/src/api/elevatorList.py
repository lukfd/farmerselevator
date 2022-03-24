from farmerselevator import application
from farmerselevator.src.helper import *

from flask import jsonify

@application.route('/getElevatorList', methods=['GET'])
def getElevatorList():
    # get names of elevators
    elevators = getElevatorArray()
    data = []
    for i in range(len(elevators)):
        data.append({"name": elevators[i][0], "address": elevators[i][1], "phone": elevators[i][2], "shopUrl": elevators[i][3]})

    # return json
    return jsonify(data)