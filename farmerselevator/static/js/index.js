// 
//  JAVASCRIPT FOR index.html
// 

// GLOBAL VARIABLES
var app;
var mymap;
var elevatorList;
var nominatimBaseUrl = 'https://nominatim.openstreetmap.org/search?';
// Minnesota Center Map
var lng = -94.648311
var lat = 46.108537

// when page loads 
function init() {

    $("#resultBox").width($('#searchBar').width());
    $(window).on('resize', function(){
        $("#resultBox").width($('#searchBar').width());
    });

    // Vue
    app = new Vue({
        el: '#app',
        data: {
          searchInput: '',
          results: [],
          discoveredResultsNames:[]
        },
        methods: {
            filterSearch: filterSearch,
            searchMap: searchMap
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

    $.get('/getElevatorList', (data) => {
        elevatorList = data
    }).then( () => {
        elevatorList.forEach( (obj) => {
            let url = nominatimBaseUrl + 'street='+ encodeURIComponent(obj.address.trim()) +'&state=MN&format=json'
            $.get( url, ( data ) => {
                if (data) {
                    obj.latlng = [data[0].lat, data[0].lon]
                } else {
                    obj.latlng = [lat, lng]
                }
                var marker = L.marker([obj.latlng[0], obj.latlng[1]], title = obj.name).addTo(mymap);
                marker.bindPopup(
                    '<h3>'+obj.name+'</h3>'+
                    '<div style="padding-top:3px;"></div>'+
                    '<a href="/shop?name='+obj.name+'">'+'visit shop'+'</a><br>'+
                    '<p>Address: '+obj.address+'</p>'+
                    '<p>Phone:'+obj.phone+'</p>', {
                    minWidth : 100,
                    autoClose: false
                });
                obj.marker = marker
            })
        })
    })
}

//---
// @return: flyTo the elevator searched
// @paramaters: app.searchInput is what the user inputted
//---
function searchMap () {
    var elevatorFound = []
    if (app.searchInput) {
        elevatorList.forEach((obj) => {
            // if name is result then go to that
            if (obj.name.toUpperCase().includes(app.searchInput.toUpperCase())) {
                obj.marker.openPopup()
                elevatorFound.push(obj)
            }
        })
        if (elevatorFound.length > 0) { // TO-DO ideally find string most similar to searchInput
            mymap.flyTo(elevatorFound[0].latlng, 15)
            app.searchInput = ''
            app.results = []
            app.discoveredResultsNames = []
        }
    }
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