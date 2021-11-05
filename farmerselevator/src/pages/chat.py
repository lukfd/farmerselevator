from farmerselevator import application
from farmerselevator import socketio
import farmerselevator.constants

import uuid
import sqlite3 as lite
from flask import render_template, session
from flask_socketio import join_room, leave_room, send

@application.route('/chat')
def chat():
    return render_template('chat.html', elevator = session['elevator'], user_id = session['user_id'])

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', to=room)

@socketio.on('message')
def handle_message(message):
    send(message)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', to=room)  