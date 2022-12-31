// code copied from the bulma documentation
$(document).ready(function () {
    // Check for click events on the navbar burger icon
    $(".navbar-burger").click(function () {
        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");
    });
    // code added by me
    $(".modal-button").click(function () {
        $(".modal").toggleClass("is-active");
    });
    $(".modal-header__close").click(function () {
        $(".modal").toggleClass("is-active");
    });
    $(".modal-footer__cancel").click(function () {
        $(".modal").toggleClass("is-active");
    });
    $("#delete-review").keydown(function (e) {
        if (e.which == 13) {
            $("#modal-card").show();
        }
    });
    $("#close-modal").keyup(function (e) {
        if (e.which == 27) {
            console.log("clicked 'delete review'");
            $("#modal-card").hide();
        }
    });
    $("#cancel").keydown(function (e) {
        if (e.which == 13) {
            $("#modal-card").hide();
        }
    });
    $("#navbar-burger").keydown(function (e) {
        if (e.which == 13) {
            $(".navbar-menu").toggleClass("is-active");
        }
    });
    $("#no-result").keydown(function (e) {
        if (e.which == 13) {
            console.log("click");
            $("#no-result-message").hide();
        }
    });
});

// get current year for Copyright info
let getYear = new Date().getFullYear();
let yearID = document.getElementById("year");
if (getYear == 2022) {
    yearID.innerHTML = `\u00A0${getYear}\u00A0`;
} else {
    yearID.innerHTML = `\u00A0 2022 - ${getYear}\u00A0`;
}
