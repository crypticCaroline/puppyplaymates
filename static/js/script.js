$(document).ready(function () {
    $(".button-collapse").sideNav();
    $('#textarea1').val('New Text');
    $('#textarea1').trigger('autoresize');
    $('select').material_select();
    $('.modal').modal();
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


like = document.getElementById('overlay_happy')
unlike = document.getElementById('overlay_angry')

function overlay_happy(){
  let form = document.getElementById('form_like')  
  console.log(form)
  like.style.display = "block";
  setTimeout(function(){ form.submit( ); }, 3000)
};

function overlay_angry(){
  let form = document.getElementById('form_dislike')  
  console.log(form)  
  unlike.style.display = "block";
  setTimeout(function(){ form.submit(); }, 3000)
};
