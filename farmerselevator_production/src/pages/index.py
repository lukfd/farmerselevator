from farmerselevator_production import application

from flask import render_template

@application.route('/')
def index():
    return render_template('index.html')