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
    var elevators;

    // Map
    // SETTING UP MAP
    latlng = L.latLng(lat, lng);
        mymap = L.map('mapid', {
        minZoom: 0,
        maxZoom: 18
    }).setView(latlng, 7);
    // boundries of the map
    var southWest = L.latLng(40, -80);
    var northEast = L.latLng(50, -110);
    var mybounds = L.latLngBounds(southWest, northEast);
    L.tileLayer('http://services.arcgisonline.com/arcgis/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
        //bounds: mybounds,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors <a href="/manage">Manage</a>',
    }).addTo(mymap);

    // getting list of elevators
    fetch('/getElevatorList')
    .then((response) => {
        return response.json();
    })
    .then((data) => { // is an array of jsons
        elevators = data
    });

    /**********************************************/
    // ELEVATOR SEARCH BAR
    /**********************************************/
    document.getElementById("elevatorSearch").addEventListener("input", elevatorSearch);

    function elevatorSearch() {
        // grab searchBar html element
        var input = this.value;
        var searchBarElement = this;

        // deleting all children of parent of input that are after the button
        for (var i = searchBarElement.parentNode.children.length - 1; i >= 2; i--) {
            searchBarElement.parentNode.children[i].remove();
        }

        // append results
        elevators.forEach((obj) => {

            // if is the same as inputted
            if (obj.name.toUpperCase().includes(input.toUpperCase()) && 
                input !== '' && input !== ' ') {
                
                // then create new element
                var newElement = document.createElement("DIV");
                // adding style (background)
                newElement.setAttribute("style", 
                "z-index: +2;" +
                "background-color: rgba(132, 138, 148, 0.3);" + 
                "width: 399px;" +
                "border-radius: 4px;" +
                "margin:auto;");

                newElement.innerHTML = '<a href="/shop?name=' + obj.name + '">' + obj.name + '</a>';
                searchBarElement.parentNode.appendChild(newElement);
            }
            
        });
    }
}

/**********************************************/
// SIGN UP MODAL
/**********************************************/ 
// Get the modal
var modal = document.getElementById('id01');
      
// if user clicks outside of form, close
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}