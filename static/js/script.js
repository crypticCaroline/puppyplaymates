$(document).ready(function () {
    $(".button-collapse").sideNav();
    $('#textarea1').val('New Text');
    $('#textarea1').trigger('autoresize');
    $('select').material_select();
    $('.chips').material_chip();
    $('.collapsible').collapsible();
    $('.modal').modal({
        // inDuration: 500
    });
    $('.datepicker').pickadate({
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 15, // Creates a dropdown of 15 years to control year,
        today: 'Today',
        clear: 'Clear',
        close: 'Ok',
        closeOnSelect: false, // Close upon selecting a date,
        container: undefined, // ex. 'body' will append picker to body
    });

})

let today = new Date();
let dd = today.getDate();
let mm = today.getMonth()+1;  
let yyyy = today.getFullYear();
// checks if the date is less than 10 so adds a 0 infront 
 if(dd<10){
        dd='0'+dd
    } 
    if(mm<10){
        mm='0'+mm
    } 

today = yyyy+'-'+mm+'-'+dd;
oldestYear = yyyy-21;
oldestDog = oldestYear+'-'+mm+'-'+dd;
eventYear = yyyy+1;
eventDate = eventYear+'-'+mm+'-'+dd;

document.getElementById("dog_dob").setAttribute("max", today);
document.getElementById("dog_dob").setAttribute("min", oldestDog);
document.getElementById("date").setAttribute("min", today);
document.getElementById("date").setAttribute("max", eventYear);


like = document.getElementById('overlay_happy')
unlike = document.getElementById('overlay_angry')

function overlay_happy() {
    let form = document.getElementById('form_like')
    like.style.display = "block";
    setTimeout(function () { form.submit(); }, 3000)
};

function overlay_angry() {
    let form = document.getElementById('form_dislike')
    unlike.style.display = "block";
    setTimeout(function () { form.submit(); }, 3000)
};

