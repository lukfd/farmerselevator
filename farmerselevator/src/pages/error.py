from farmerselevator import application
from farmerselevator.src.helper import *

@application.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return """
    <link rel="stylesheet" type="text/css" href="/static/css/main.css">
    <h1>Page not found...</h1>
    <nav>
        <a href="/home" type="button">Home</a>
        <a href="/signin" type="button">Sign In</a>
        <a href="/signup" type="button">Sign Up</a>
    </nav>
    """