var button = document.getElementById("btnTurno");
 
button.addEventListener("click", function() {
    alert("Button Clicked!");
});

function GrabaTurno(idTurno) {
    let currentDate2 = new Date().toJSON().slice(0, 10);
    console.log(currentDate2); // "2022-06-17"

    alert(idTurno + " " + currentDate2);

}
