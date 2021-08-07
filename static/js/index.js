// 
//  JAVASCRIPT FOR index.html
// 

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