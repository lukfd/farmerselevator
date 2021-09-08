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

###############################################
# IMPORTS
from flask import Flask

from website.website import Website
from database.database import Database

# Flask name server
app = Flask(__name__)

# CONSTANTS
app.secret_key = b'b[\x0e\x8c\x87\xdb\xa17\x9a\x8d\xdeO\r\xba|\xcd'
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

##################################################
#                                                #
#  METHODS LIST and ports of the API:            #
#                                                #
#  # # # # # # # # # # # # # # # # # # # # # # # #  
#  
#  WEBSITE:
#   def __init__(self, app):
#
#   @app.route('/')  
#   def index(self):
#
#   @app.route('/contact-us') 
#   def contact_us(self):
#
#   @app.route('/signin') 
#   def signin(self):
#
#   @app.route('/signup') 
#   def signup(self):
#
#   @app.route('/logout') 
#   def logout(self):
#
#   @app.route('/settings-elevator') 
#   def settings_elevator():
#
#   @app.route('/settings-farmer') 
#   def settings_farmer():
#
#   @app.route('/get-profile-image/<file>') 
#   def get_profile_image(self, file):
#
#   @app.route('/home') 
#   def homepage():
#
#   @app.route('/shop', methods=['GET']) 
#   def shop():
#
#   @app.route('/buy/<int:product_id>/<int:elevator_id>', methods=['GET', 'POST']) 
#   def buy(product_id, elevator_id):
#
#   @app.route('/submit-order/<int:product_id>/<int:elevator_id>/<int:farmer_id>', methods=['GET', 'POST']) 
#   def submit_order(product_id, elevator_id, farmer_id):
#
#   @app.route('/manage-shop') 
#   def manage_shop():
#
#   @app.errorhandler(404) 
#   def page_not_found(e):
#
# DATABASE:
#   
#   def __init__(self, app):
#
#   @app.route('/signin-form', methods=['POST'])
#   def signin_form():
#   
#   @app.route('/signup-form', methods=['POST'])
#   def signup_form():
#   
#   @app.route('/contact-us-message', methods=['POST'])
#   def contact_us_message(self):
#   
#   @app.route('/change-profile-information', methods=['POST'])
#   def change_profile_information():
#   
#   @app.route('/change-profile-image', methods=['POST'])
#   def change_profile_image(self):
#   
#   @app.route('/change-password', methods=['GET', 'POST', 'PULL'])
#   def change_password():
#   
#   @app.route('/delete-account')
#   def delete_account():
#   
#   @app.route('/getElevatorList', methods=['GET'])
#   def getElevatorList():
#   
#   @app.route('/profile/<string:id>', methods=['GET'])
#   def profile(id):
#   
#   @app.route('/mark-completed', methods=['GET'])
#   def mark_completed():
#   
#   @app.route('/add-product', methods=['POST'])
#   def add_product():
#   
#   @app.route('/update-product', methods=['POST'])
#   def update_product():
#   
#   @app.route('/delete-product/<int:elevator_id>/<int:product_id>', methods=['GET','POST'])
#   def delete_product(elevator_id, product_id): 
#
# HELPER:
#   def closeSession():
#   def getProductList(id):
#   def getProductInformation(product_id, elevator_id):
#   def getProductName(elevator_id, product_id):
#   def deleteProduct(elevator_id, product_id):
#   def insertNewOrder(order_id, product_id, elevator_id, farmer_id, quantity_requested, measure, description, product_name):
#   def markAsComplete(product_id, elevator_id, order_id):
#   def elevatorGetOrders(elevator_id):
#   def farmerGetOrders(farmer_id):
#   def substituteWithOlderValues(toUpdate, olderValues):
#   def getElevatorArray():
#
#####################################################

# WEBSITE MAIN FUNCTIONS

Website(app)
Database(app)