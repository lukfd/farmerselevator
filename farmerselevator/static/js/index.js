// 
//  JAVASCRIPT FOR index.html
// 

// GLOBAL VARIABLES
var mymap;
// Minnesota Center Map
var lng = -94.648311
var lat = 46.108537

// when page loads 
function init() {

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