from flask_socketio import send
from farmerselevator import application
from farmerselevator import socketio

from flask import render_template

@application.route('/chat')
def chat():
    return render_template('chat.html')

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)
    send(data,broadcast=True)