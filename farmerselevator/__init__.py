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

from flask import Flask
application = Flask(__name__)

# internal functions for api and pages calls
import farmerselevator.src.api.buy
import farmerselevator.src.api.elevatorList
import farmerselevator.src.api.orders
import farmerselevator.src.api.products
import farmerselevator.src.api.registration
import farmerselevator.src.api.settings

import farmerselevator.src.pages.index
import farmerselevator.src.pages.logout
import farmerselevator.src.pages.registration
import farmerselevator.src.pages.settings
import farmerselevator.src.pages.shop
import farmerselevator.src.pages.profile
import farmerselevator.src.pages.manageShop
import farmerselevator.src.pages.error
import farmerselevator.src.pages.contactus
import farmerselevator.src.pages.home

# running the server
if __name__ == '__main__':
    application.run()