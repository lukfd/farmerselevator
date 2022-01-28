#    Written by Luca Comba and Daniel Taufiq
#    started May 2021

###############################################
#  This is the server for the website         #
#                                             #
#  It uses flask, sqlite and our written      #
#  helper methods.                            #
#                                             #
#  for more infromation visit:                #
#  https://github.com/lukfd/farmerselevator_production   #
###############################################

from flask import Flask
from flask_socketio import SocketIO

application = Flask(__name__)
socketio = SocketIO(application)

# internal functions for api and pages calls
import farmerselevator_production.src.api.buy
import farmerselevator_production.src.api.elevatorList
import farmerselevator_production.src.api.orders
import farmerselevator_production.src.api.products
import farmerselevator_production.src.api.registration
import farmerselevator_production.src.api.settings
import farmerselevator_production.src.api.usersUtils
import farmerselevator_production.src.api.chatUtils

import farmerselevator_production.src.pages.index
import farmerselevator_production.src.pages.about
import farmerselevator_production.src.pages.terms
import farmerselevator_production.src.pages.logout
import farmerselevator_production.src.pages.registration
import farmerselevator_production.src.pages.settings
import farmerselevator_production.src.pages.shop
import farmerselevator_production.src.pages.profile
import farmerselevator_production.src.pages.manageShop
import farmerselevator_production.src.pages.error
import farmerselevator_production.src.pages.contactus
import farmerselevator_production.src.pages.home
import farmerselevator_production.src.pages.chat
import farmerselevator_production.src.pages.test

# running the server
if __name__ == '__main__':
    #application.run()
    socketio.run(application, host='0.0.0.0', port='8000', debug=True)