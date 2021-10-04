# Server

Endpoints and functions

### Adding a new page or API function
To add a new web page or a API route, you will need to create a python script into either `/pages` or `/api`.
Then you will need to also add the reference to the script into the `__init__.py` script such as: 

```import farmerselevator.src.pages.newpagename```

### Pages

```
def __init__(self, app):

@app.route('/')  
def index(self):

 @app.route('/contact-us') 
def contact_us(self):

 @app.route('/signin') 
def signin(self):

 @app.route('/signup') 
def signup(self):

 @app.route('/logout') 
def logout(self):

 @app.route('/settings-elevator') 
def settings_elevator():

 @app.route('/settings-farmer') 
def settings_farmer():

 @app.route('/get-profile-image/<file>') 
def get_profile_image(self, file):

 @app.route('/home') 
def homepage():

 @app.route('/shop', methods=['GET']) 
def shop():

 @app.route('/buy/<int:product_id>/<int:elevator_id>', methods=['GET', 'POST']) 
def buy(product_id, elevator_id):

 @app.route('/submit-order/<int:product_id>/<int:elevator_id>/<int:farmer_id>', methods=['GET', 'POST']) 
def submit_order(product_id, elevator_id, farmer_id):

 @app.route('/manage-shop') 
def manage_shop():

 @app.errorhandler(404) 
def page_not_found(e):
```

### API FUNCTIONS

```
 @app.route('/signin-form', methods=['POST'])
def signin_form():

@app.route('/signup-form', methods=['POST'])
def signup_form():

@app.route('/contact-us-message', methods=['POST'])
def contact_us_message(self):

@app.route('/change-profile-information', methods=['POST'])
def change_profile_information():

@app.route('/change-profile-image', methods=['POST'])
def change_profile_image(self):

@app.route('/change-password', methods=['GET', 'POST', 'PULL'])
def change_password():

@app.route('/delete-account')
def delete_account():

@app.route('/getElevatorList', methods=['GET'])
def getElevatorList():

@app.route('/profile/<string:id>', methods=['GET'])
def profile(id):

@app.route('/mark-completed', methods=['GET'])
def mark_completed():

@app.route('/add-product', methods=['POST'])
def add_product():

@app.route('/update-product', methods=['POST'])
def update_product():

@app.route('/delete-product/<int:elevator_id>/<int:product_id>', methods=['GET','POST'])
def delete_product(elevator_id, product_id): 
```

**helper.py**
```
def closeSession():
def getProductList(id):
def getProductInformation(product_id, elevator_id):
def getProductName(elevator_id, product_id):
def deleteProduct(elevator_id, product_id):
def insertNewOrder(order_id, product_id, elevator_id, farmer_id, quantity_requested, measure, description, product_name):
def markAsComplete(product_id, elevator_id, order_id):
def elevatorGetOrders(elevator_id):
def farmerGetOrders(farmer_id):
def substituteWithOlderValues(toUpdate, olderValues):
def getElevatorArray():
```

### References

[https://flask.palletsprojects.com/en/2.0.x/patterns/packages/#](https://flask.palletsprojects.com/en/2.0.x/patterns/packages/#)