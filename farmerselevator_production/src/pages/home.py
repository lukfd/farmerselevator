from farmerselevator_production import application
from farmerselevator_production.src.helper import *

from flask import render_template

@application.route('/home')
def homepage():
    # check if user is in session
    if 'username' in session:
        # Two different pages for elevator or farmer
        if session["elevator"] == True:
            orders = elevatorGetOrders(session["user_id"])
            return render_template('home-elevator.html', username=session["username"], id=session["user_id"], orders=orders, isElevator=session["elevator"])
        else:
            # get list of elevators
            elevators = getElevatorArray()
            correctElevators = []
            for i in elevators:
                for tuple in i:
                    correctElevators.append(tuple)
            elevators = correctElevators
            # get list of orders
            orders = farmerGetOrders(session["user_id"])

            return render_template('home-farmer.html', username=session["username"], id=session["user_id"], elevators=elevators, orders=orders, isElevator=session["elevator"])
    else:
        return redirect("/", code=302)