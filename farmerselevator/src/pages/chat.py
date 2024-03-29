from farmerselevator import application
from farmerselevator import socketio
from farmerselevator import mysql
import farmerselevator.constants
from farmerselevator.src.helper import getUserId, convertIsElevator

from flask import render_template, session, redirect
from flask_socketio import join_room, leave_room, send, emit

# HELPER FUNCTION

def saveChat(room_id, farmer_id, elevator_id):
    cur = mysql.get_db().cursor()

    cur.execute("INSERT INTO chats (room_id, farmer_id, elevator_id) VALUES (%s, %s, %s);", (room_id, farmer_id, elevator_id,))
    cur.close()
    return

def updateMessageHistory(newMessage, room):

    # TO-DO: check if room actually exists

    cur = mysql.get_db().cursor()

    cur.execute("SELECT messages FROM chats WHERE room_id=%s;", (room,))
    result = cur.fetchone()[0]
    if result is None:
        messages = newMessage
    else:
        messages = result + '\n' + newMessage
    cur.close()

    cur = mysql.get_db().cursor()
    cur.execute('UPDATE chats SET messages=%s WHERE room_id=%s;', (messages, room,))
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