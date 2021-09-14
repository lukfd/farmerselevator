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


##################################################
#                                                #
#  METHODS LIST and ports of the API:            #
#                                                #
#  # # # # # # # # # # # # # # # # # # # # # # # #  
#  
#  index():
#  contact_us():
#  contact_us_message():
#  signin():
#  signup():
#  logout():
#  signin_form():
#  signup_form():
#
#  settings_elevator():
#  settings_farmer():
#  change_profile_information():
#  change_profile_image():
#  get_profile_image(file):
#  change_password():
#  delete_account():
#  homepage():
#  getElevatorList():
#  profile(id):
#  shop():
#  buy(product_id, elevator_id)
#  submit_order(product_id, product_id)
#  mark_completed():
#  manage_shop():
#  add_product():
#  update_product():
#  delete_product(elevator_id, product_id)
#  page_not_found(e):
#
#####################################################

if __name__ == '__main__':
    application.run()