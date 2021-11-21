# Socket.io connections

### A breif description

Under `/src/pages` we use the **chat.py** that uses flask-socketio library to manage all the messages between farmers and elevators.

It will be also implemented the socket io to update autmagically the `/home` which will be tight to the buy and orders coming in and out.

### How it works

Think of a room as an array of users that stays on the server. When you send your message in "send message", you set broadcast=True, so it sends it as a global message to all users, as long as they are connected. If you only want to send to users in specific rooms, you will need to specify which room you want to send the message to from the client, each time you send a message, like this:

*client.js*
```
socket.emit('join', { 'channel': channel, ... });
socket.emit('send message', {'message': message, 'channel': channel});
```

*server.py*
```
@socketio.on("send message")
def message(data):
    room = data['channel']
    emit('broadcast message', data['message'], room=room)
```

> cit - [Jacob Sussan](https://stackoverflow.com/questions/53807546/concise-example-of-how-to-join-and-leave-rooms-using-flask-and-socket-io)

### CDN

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js" 
    integrity="sha512-q/dWJ3kcmjBLU4Qc47E4A9kTB4m3wuTY7vkFJDTZKjTs8jhyGQnaUrxa0Ytd0ssMZhbNua9hE+E7Qv1j+DyZwA==" 
    crossorigin="anonymous"></script>
```

---

### Resources

- a good explanation about rooms [link](https://stackoverflow.com/questions/53807546/concise-example-of-how-to-join-and-leave-rooms-using-flask-and-socket-io)
- [https://stackoverflow.com/questions/53807546/concise-example-of-how-to-join-and-leave-rooms-using-flask-and-socket-io](https://stackoverflow.com/questions/53807546/concise-example-of-how-to-join-and-leave-rooms-using-flask-and-socket-io)
- https://stackoverflow.com/questions/30124701/how-to-emit-websocket-message-from-outside-a-websocket-endpoint