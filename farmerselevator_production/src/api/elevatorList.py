from farmerselevator_production import application
from farmerselevator_production.src.helper import *

from flask import jsonify

@application.route('/getElevatorList', methods=['GET'])
def getElevatorList():
    # get names of elevators
    elevators = getElevatorArray()

    data = []
    for i in range(len(elevators)):
        data.append({"name": elevators[i][0]})

    # return json
    return jsonify(data)