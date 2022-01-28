from farmerselevator import application
from farmerselevator import socketio
import farmerselevator.constants
from farmerselevator.src.helper import getUserId, convertIsElevator

import sqlite3 as lite
from flask import render_template, session, redirect
from flask_socketio import join_room, leave_room, send, emit

# HELPER FUNCTION

def saveChat(room_id, farmer_id, elevator_id):
    con = lite.connect(farmerselevator.constants.databasePath) 
    cur = con.cursor()

    cur.execute("INSERT INTO chats (room_id, farmer_id, elevator_id) VALUES (?, ?, ?);", (room_id, farmer_id, elevator_id,))
    con.commit()
    cur.close()
    return

def updateMessageHistory(newMessage, room):

    # TO-DO: check if room actually exists

    con = lite.connect(farmerselevator.constants.databasePath) 
    cur = con.cursor()

    cur.execute("SELECT messages FROM chats WHERE room_id=?;", (room,))
    result = cur.fetchone()[0]
    if result is None:
        messages = newMessage
    else:
        messages = result + '\n' + newMessage
    cur.close()

    con = lite.connect(farmerselevator.constants.databasePath) 
    cur = con.cursor()
    cur.execute('UPDATE chats SET messages=? WHERE room_id=?;', (messages, room,))
    con.commit()
    cur.close()

# MAIN FUNCTION

@application.route('/chat')
def chat():
    if 'elevator' in session:
        return render_template('chat.html', elevator=session['elevator'], user_id=session['user_id'])
    else:
        return redirect("/")

@socketio.on('newchat')
def on_new_chat(data):
    isElevator = convertIsElevator(data['isElevator'])
    fromUserId = data['fromUserId']
    toUser = data['toUser']
    room = data['room']
    join_room(room)

    if isElevator:
        elevator_id = fromUserId
        farmer_id = getUserId(toUser, not isElevator)
    else:
        farmer_id = fromUserId
        elevator_id = getUserId(toUser, not isElevator)

    saveChat(room, farmer_id, elevator_id)

    emit('alert', fromUserId + ' has entered the room.', room=room)

    # get toUserId
    toUserId = getUserId(toUser, not isElevator)
    emit('incoming new chat', {'toUserId': toUserId, 'isElevator': not isElevator, 'room': room}, broadcast=True)

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('alert', 'entered the room.', room=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    message = data['message']
    fromUser = data['fromUser']

    updateMessageHistory(message, room)

    emit('broadcast message', {"message": message, "fromUser": fromUser}, room=room)

@socketio.on('leave')
def on_leave(data):
    userId = data['userId']
    room = data['room']
    leave_room(room)
    emit('alarm', userId + ' has left the room.', room=room)