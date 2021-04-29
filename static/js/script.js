// Initialise materlize features and a few functions to aid user experience

$(document).ready(function () {
    $(".button-collapse").sideNav();
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

});

// Show more functionality for playmates page
$(function () {
    $(".user-list .user-cards").slice(0, 10).css('display', 'flex');
    $("#loadMore").on('click', function (e) {
        e.preventDefault();
        $(".user-list .user-cards:hidden").slice(0, 6).css('display', 'flex');
        if ($(".user-list .user-cards:hidden").length == 0) {
            $("#load").fadeOut('slow');
            $("#loadMore").fadeOut('slow');
        }
    });
});

// Show more for comments
$(function () {
    $(".comment-area .comments").slice(0, 3).css('display', 'block');
    if ($(".comment-area .comments:hidden").length == 0) {
        $("#loadMore").css('display', 'none');
    }
    $("#loadMore").on('click', function (e) {
        e.preventDefault();
        $(".comment-area .comments:hidden").slice(0, 3).css('display', 'block');
        if ($(".comment-area .comments:hidden").length == 0) {
            $("#load").fadeOut('slow');
            $("#loadMore").fadeOut('slow');
        }
    });
});

// Toggle to top
$('#top-toggle').click(function () {
    $('body,html').animate({
        scrollTop: 0
    }, 1200);
    return false;
});

$(window).scroll(function () {
    if ($(this).scrollTop() > 50) {
        $('#top-toggle').fadeIn();
    } else {
        $('#top-toggle').fadeOut();
    }
});

$(function () {
    $('.comments-area .comments').each(function () {
        if ($(this).is(':empty')) {
            $(this).css('display', 'none')
        }
    })
});
    

// Overylay Gif function
like = document.getElementById('overlay_happy');
unlike = document.getElementById('overlay_angry');

function overlayHappy() {
    let form = document.getElementById('form_like');
    like.style.display = "block";
    setTimeout(function () { form.submit(); }, 3000);
};

function overlayAngry() {
    let form = document.getElementById('form_dislike');
    unlike.style.display = "block";
    setTimeout(function () { form.submit(); }, 3000);
};

// Date pickers
let today = new Date();
let dd = today.getDate();
let mm = today.getMonth() + 1;
let yyyy = today.getFullYear();
// checks if the date is less than 10 so adds a 0 in front 
if (dd < 10) {
    dd = '0' + dd;
}
if (mm < 10) {
    mm = '0' + mm;
}

today = yyyy + '-' + mm + '-' + dd;
oldestYear = yyyy - 21;
oldestDog = oldestYear + '-' + mm + '-' + dd;
eventYear = yyyy + 1;
eventDate = eventYear + '-' + mm + '-' + dd;

function dogDob() {
    document.getElementById("dog_dob").setAttribute("max", today);
    document.getElementById("dog_dob").setAttribute("min", oldestDog);
}

function walkDate() {
    document.getElementById("walk_date").setAttribute("min", today);
    document.getElementById("walk_date").setAttribute("max", eventDate);
}