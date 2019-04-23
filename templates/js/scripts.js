$(function () {
    const body = $("body");

    body.removeClass("loading");

    $("#more-info-trigger").click(function () {
        body.toggleClass("more-info-active")
    });
});

