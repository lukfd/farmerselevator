// 
//  JAVASCRIPT FOR chat
// 

// GLOBAL VARIABLES
var app;
var socket = io();

// when page loads 
function init() {

    socket.on('connect', () => {
        //socket.emit('my event', {data: 'I\'m connected!'});
        socket.send('Im connected')
    });

    socket.on('message', (message) => {
        console.log('message received ' + message)
        app.messages.push(message)
    })

    // Vue
    app = new Vue({
        el: '#app',
        data: {
            messageToSend: '',
            messages: []
        },
        methods: {
            sendMessage: () => {
                //console.log('sending ' + app.messageToSend + ' ...')
                socket.send(app.messageToSend);
                //console.log('sent!')
            }
        }
    })
}