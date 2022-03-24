// 
//  JAVASCRIPT FOR index.html
// 

// GLOBAL VARIABLES
var app;
var mymap;
var elevatorList;
// Minnesota Center Map
var lng = -94.648311
var lat = 46.108537

// when page loads 
function init() {

    $("#resultBox").width($('#searchBar').width());
    $(window).on('resize', function(){
        $("#resultBox").width($('#searchBar').width());
    });

    $.get('/getElevatorList', (data) => {
        elevatorList = data
    })

    // Vue
    app = new Vue({
        el: '#app',
        data: {
          searchInput: '',
          results: [],
          discoveredResultsNames:[]
        },
        methods: {
            filterSearch: filterSearch
        }
    })

    // Map
    // SETTING UP MAP
    latlng = L.latLng(lat, lng);
        mymap = L.map('mapid', {
        minZoom: 0,
        maxZoom: 18,
        zoomControl: false
    }).setView(latlng, 7);
    // boundries of the map
    var southWest = L.latLng(40, -80);
    var northEast = L.latLng(50, -110);
    var mybounds = L.latLngBounds(southWest, northEast);
    L.tileLayer('http://services.arcgisonline.com/arcgis/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
        //bounds: mybounds,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(mymap);
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