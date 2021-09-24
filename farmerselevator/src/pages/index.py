from farmerselevator import application

from flask import render_template

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/try')
def test():
    return render_template('try.html')