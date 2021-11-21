// 
//  JAVASCRIPT FOR homepage
// 

// GLOBAL VARIABLES
// It includes also the one from html: username, userId, isElevator
// which they carry information of the logged in user, using this home page.
var app
var socket = io()

// when page loads 
function init() {

    console.log("isElevator: " + isElevator)
    console.log("userId: " + userId)
    console.log("username: " + username)

    $.get('/getElevatorList', (data) => {
        elevatorList = data
    })

    // if another user have opened a new chat with you
    // data will be: {'farmerId': farmer_id, 'elevatorId': elevator_id}
    socket.on('incoming new order', (data) => {
        console.log('Incoming new order!' + JSON.stringify(data))

        if (isElevator == "True") {
            console.log("isElevator true for incoming new order")
            // check for farmer_id
            if (data.elevatorId == userId) {
                // refresh page
                window.location.reload();
            }
        } else {
            if (data.farmerId == userId) {
                // refresh page
                window.location.reload();
            }
        }
    })

    // Vue
    app = new Vue({
        el: '#app',
        data: {
          searchInput: '',
          showNewOrders: true,
          results: [],
          discoveredResultsNames:[]
        },
        methods: {
            filterSearch: filterSearch,
            setNewOrdersTrue: () => app.showNewOrders = true,
            setNewOrdersFalse: () => app.showNewOrders = false
        }
    })
}


//---
// @return: add what it finds to app.results
// @paramaters:
//      app.searchInput is what the user inputted
//      elevatorList is the full list of elevators
//---
function filterSearch () {

    if (app.searchInput === ' ' || app.searchInput === '') {
        app.results = []
        app.discoveredResultsNames = []
    }

    elevatorList.forEach((obj) => {
        // if is the same as inputted
        if (obj.name.toUpperCase().includes(app.searchInput.toUpperCase()) &&
         app.searchInput !== '' && app.searchInput !== ' ' &&  !app.discoveredResultsNames.includes(obj.name)) {
            app.results.push({name: obj.name, link: '/shop?name='+obj.name})
            app.discoveredResultsNames.push(obj.name)
        }
    });
}