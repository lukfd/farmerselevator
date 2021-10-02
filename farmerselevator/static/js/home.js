// 
//  JAVASCRIPT FOR homepage
// 

// GLOBAL VARIABLES
var app;

// when page loads 
function init() {

    console.log('Hello');

    $.get('/getElevatorList', (data) => {
        elevatorList = data
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