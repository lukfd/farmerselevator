/*   

    JAVASCRIPT FOR chat page.

    DESCRIPTION:
        Here farmers will be able to start a chat with a 
        elevator, and an elevator will be able to start a chat
        with a farmer.

        It uses socket io and functions in chat.py and chatUtils.py

    TODO:
        - send info about who sent what

*/ 

// VARIABLES FROM CHAT.PY
// userId and isElevator

// GLOBAL VARIABLES
var app
var socket = io()

// HELPERS
function createNewUuidRoom () {
    return uuidv4()
}

// @return: true if chat already exists between them, false otherwise
function isChat(fromUserId, isElevator, toUser) {
    return new Promise ( (resolve, reject) => {
        var data = {"fromUserId": fromUserId, "isElevator": isElevator, "toUser": toUser}
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/isChat',
            dataType : 'json',
            data : JSON.stringify(data),
            success : (data) => {
                console.log('isChat response: ' + data.return)
                if (data.return == 'True') {
                    resolve(true)
                } else if ( data.return == 'False') {
                    resolve(false)
                } else {
                    reject(data.return)
                } 
            },
            error : (data) => {
                console.log(data)
                reject(data)
            }
        })
    })
}

// @return: uuid if chat exists or error if does not
function getRoom(fromUserId, isElevator, toUser) {
    return new Promise ( (resolve, reject) => {
        var data = {"fromUserId": fromUserId, "isElevator": isElevator, "toUser": toUser}
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/getRoom',
            dataType : 'json',
            data : JSON.stringify(data),
            success : (data) => {
                console.log( "getRoom response: " + data.return )
                resolve(data.return)
            },
            error : (data) => {
                console.log(data)
                reject(data)
            }
        })
    })
}

// @return messages, a string
function getPreviousMessages(room) {
    return new Promise ( (resolve) => {
        var data = {"room": room}
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/getPreviousMessages',
            dataType : 'json',
            data : JSON.stringify(data),
            success : (data) => {
                console.log( "getPreviousMessages response: " + data.messages )
                resolve(data.messages)
            },
            error : (data) => {
                console.log('Error getPreviousMessages: ' + data)
                reject(data)
            }
        })
    })
}

// @return an array of json composed by {toUser: toUser, room: room}
function loadRooms(fromUserId, isElevator) {
    return new Promise ( (resolve) => {
        var data = {"fromUserId": fromUserId, "isElevator": isElevator}
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/loadRooms',
            dataType : 'json',
            data : JSON.stringify(data),
            success : (data) => {
                console.log( "loadRooms response: " + data )
                resolve(data)
            },
            error : (data) => {
                console.log('Error loadRooms: ' + data)
                reject(data)
            }
        })
    })
}

// @return: true if username exists, false otherwise
function usernameExists(toUser, isElevator) {
    return new Promise ( (resolve, reject) => {
        let oppositeIsElevator
        if (isElevator === "True") {
            oppositeIsElevator = "False"
        } else {
            oppositeIsElevator = "True"
        }

        var data = {"username": toUser, "isElevator": oppositeIsElevator}
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/userExists',
            dataType : 'json',
            data : JSON.stringify(data),
            success : (data) => {
                console.log("usernameExists returned:" + data.return)
                if (data.return == "True") {
                    resolve(true)
                } else if (data.return == "False") {
                    resolve(false)
                } else {
                    resolve(false)
                }
            },
            error : (data) => {
                console.log(data)
                reject(data)
            }
        });
    })
}

// when page loads 
function init() {


    // start listening if we get any new messages
    socket.on('broadcast message', (data) => {
        console.log('BROADCAST MESSAGE: ' + JSON.stringify(data))
        app.messages.push(data.message)
    })

    // logging alerts
    socket.on('alert', (data) => {
        console.log(data)
    })

    // if another user have opened a new chat with you
    socket.on('incoming new chat', (data) => {
        console.log('Incoming new chat!' + JSON.stringify(data))
        let isElevatorBool
        if (isElevator == 'True') {
            isElevatorBool = true
        } else {
            isElevatorBool = false
        }

        if (data.toUserId == userId && data.isElevator == isElevatorBool) {
            console.log("isElevator: " + isElevatorBool)
            
            loadRooms(app.fromUserId, app.isElevator).then( (res, rej) => {
                console.log("loadingroom: " + res)
                if (res) {
                    app.rooms = res
                }
                if (rej) {
                    console.log('LOAD ROOMS error: ' + rej)
                }
            })
        }
    })

    // Vue
    app = new Vue({
        el: '#app',
        data: {
            isElevator: isElevator,
            fromUserId: userId,
            toUser: '',
            messageToSend: '',
            messages: [],
            roomOpen: '',
            roomOpenUsername: '',
            rooms: []
        },
        methods: {
            sendMessage: function () {
                socket.emit('message', {message: app.messageToSend, fromUser: app.fromUserId, room: app.roomOpen}, () => {
                    console.log('MESSAGE SENT: ' + app.messageToSend + ', FROM ' + app.fromUserId + ', ROOM ' + app.roomOpen)
                    app.messageToSend = ''
                })
            },
            openChat: function (room) {
                console.log('OPEN CHAT @' + room)
                
                app.messages = []
                app.roomOpen = room

                // find username
                app.rooms.forEach(element => {
                    if (element.room === app.roomOpen) {
                        app.roomOpenUsername = element.toUser
                    }
                })
                
                // load history of messages
                getPreviousMessages(room).then( (res, rej) => {
                    console.log(' WHAT IS RES : ' + (typeof res))
                    if (res || res == undefined) {
                        if ( res !== undefined) {
                            let array = res.split('\n')
                            for (let message of array) {
                                app.messages.push(message)
                            }
                        }
                    } else {
                        console.log(rej)
                    }
                    socket.emit('join', {room: room})
                })
            },
            search: function () { 

                // does app.toUser exsists?
                usernameExists(app.toUser, app.isElevator).then( (res, rej) => {
                    
                    if (res) {
                    
                        // check if a chat between app.fromUserId and app.toUser already exists
                        isChat(app.fromUserId, app.isElevator, app.toUser).then( (res, rej) => {
                            console.log('WHAT IS RES? ' + res)
                            if (res) {
                                console.log('INDEED IS CHAT!')
                                // if there is, load previous messages.
                                getRoom(app.fromUserId, app.isElevator, app.toUser).then( (room) => {
                                    this.openChat(room)
                                    // https://stackoverflow.com/questions/40707738/vuejs-accessing-a-method-from-another-method/40708474
                                })
                            } else if (rej) {
                                console.log('IS CHAT REJECTED FOR: ' + rej)
                            } else {
                                // There are no chat
                                // room to join
                                app.roomOpen = createNewUuidRoom()
                                
                                console.log('SEARCHING: fromUserId: ' + app.fromUserId + ', toUser: ' + app.toUser + ' roomOpen: ' + app.roomOpen)
                                
                                // if not in rooms, this should be almost impossible
                                if (!app.rooms.includes(app.roomOpen)) {
                                    // add it to the list
                                    app.rooms.push({toUser: app.toUser, room: app.roomOpen})
                                } else {
                                    console.log('ERROR: ' + app.roomOpen + ' UUID ALREADY EXISTS!')
                                }

                                // creating new chat
                                socket.emit('newchat', {fromUserId: app.fromUserId, isElevator: app.isElevator, toUser: app.toUser, room: app.roomOpen}, () => {
                                    app.toUser = ''
                                })
                            } 
                        })
                    
                    } else { // does not exists
                        alert("Sorry, username not found.")
                        app.toUser = ''
                    }
                }) // end of usernameExists
            }
        }
    })

    // Load chats for user
    loadRooms(app.fromUserId, app.isElevator).then( (res, rej) => {
        if (res) {
            app.rooms = res
        }
        if (rej) {
            console.log('LOAD ROOMS error: ' + rej)
        }
    })
}

function close() {
    // when windows closes, leave the room
    socket.emit('leave', {userId: app.fromUserId , room: app.roomOpen})
}