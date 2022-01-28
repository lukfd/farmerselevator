from farmerselevator import application
from farmerselevator.src.helper import *

@application.route('/logout')
def logout():
    # remove the username from the session if it's there
    closeSession()
    return redirect("/", code=302) 