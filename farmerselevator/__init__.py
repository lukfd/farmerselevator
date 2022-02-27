#    Written by Luca Comba and Daniel Taufiq
#    started May 2021

###############################################
#  This is the server for the website         #
#                                             #
#  It uses flask, sqlite and our written      #
#  helper methods.                            #
#                                             #
#  for more infromation visit:                #
#  https://github.com/lukfd/farmerselevator   #
###############################################

import os
from dotenv import load_dotenv
from flask import Flask
from flask_socketio import SocketIO
from flaskext.mysql import MySQL

application = Flask(__name__)
socketio = SocketIO(application)

# Loding env variables
load_dotenv()

# Loading DB
mysql = MySQL(autocommit=True)
application.config['MYSQL_DATABASE_USER'] = os.getenv('USERNAME')
application.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('PASSWORD')
application.config['MYSQL_DATABASE_DB'] = os.getenv('NAME')
application.config['MYSQL_DATABASE_HOST'] = os.getenv('HOST')
application.config['MYSQL_DATABASE_CHARSET'] = "utf8"
mysql.init_app(application)

# internal functions for api and pages calls
import farmerselevator.src.api.buy
import farmerselevator.src.api.elevatorList
import farmerselevator.src.api.orders
import farmerselevator.src.api.products
import farmerselevator.src.api.registration
import farmerselevator.src.api.settings
import farmerselevator.src.api.usersUtils
import farmerselevator.src.api.chatUtils

import farmerselevator.src.pages.index
import farmerselevator.src.pages.about
import farmerselevator.src.pages.terms
import farmerselevator.src.pages.logout
import farmerselevator.src.pages.registration
import farmerselevator.src.pages.settings
import farmerselevator.src.pages.shop
import farmerselevator.src.pages.profile
import farmerselevator.src.pages.manageShop
import farmerselevator.src.pages.error
import farmerselevator.src.pages.contactus
import farmerselevator.src.pages.home
import farmerselevator.src.pages.chat
import farmerselevator.src.pages.test

# running the server
if __name__ == '__main__':
    # Running
    socketio.run(application, host='0.0.0.0', port='8000', debug=True)