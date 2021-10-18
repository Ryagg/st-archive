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
});
