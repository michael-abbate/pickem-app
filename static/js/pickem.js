function allowDrop(ev) {
    ev.preventDefault();
  }
  
function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
  }
  
function drop(ev,selfid) {
    ev.preventDefault();
    // x is the object being dragged
    var x = document.getElementById(selfid);
    // data is the element getting dropped onto
    var data = ev.dataTransfer.getData("text");
    x.innerHTML = '';
    ev.target.appendChild(document.getElementById(data).cloneNode(true));
    x.style.border = "solid 2px black";  
    dragged_elem = document.getElementById(data);
    // dragged_elem..draggable="false";

    // set drag stuff here on 'data'
    // document.getElementById(data).ondrop = drop(ev,document.getElementById(data));
    // document.getElementById(data).ondragover=allowDrop(ev);
}

function changeBackground(id) {
    var input_id = "input-"+id;
    var label_id = "label-"+id;
    var input_elem = document.getElementById(input_id);
    var label_elem = document.getElementById(label_id);
    if (input_elem.checked) {
        label_elem.style.backgroundColor="dodgerblue";
        label_elem.style.color="white";
    } else {
        label_elem.style.backgroundColor="white";
        label_elem.style.color="darkslategrey";

    }
}