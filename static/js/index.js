// 
//  JAVASCRIPT FOR index.html
// 

// when page loads 
function init() {
    var elevators;

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
        for (var i = 2; i < searchBarElement.parentNode.children.length; i++) {
            console.log("deleted")
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
                newElement.setAttribute("style", "background-color: rgba(132, 138, 148, 0.3);" + 
                "width: 399px;" + "border-radius: 4px;");
                
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