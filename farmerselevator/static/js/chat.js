// 
//  JAVASCRIPT FOR chat
// 

// GLOBAL VARIABLES
var app;
var messages = [];
var socket = io();

// when page loads 
function init() {

    socket.on('message', (data) => {
        console.log(data)
    });

    // Vue
    app = new Vue({
        el: '#app',
        data: {
            isElevator: false,
            toUser: '',
            messageToSend: '',
            messages: messages
        },
        methods: {
            search: () => { 
                console.log('SEARCHING')
                socket.emit('join', {username: 'Luca', room: 'test'})
            },
            sendMessage: () => {
                console.log('MESSAGE SENT')
                socket.emit('message', {data: app.messageToSend})
            }
        }
    })
}