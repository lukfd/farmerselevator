from farmerselevator import application

from flask import render_template

@application.route('/test')
def test():
    return render_template('test.html')