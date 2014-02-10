$("#home").click(function () {
        $("#about").removeClass("active");
        $("#work").removeClass("active");
        $("#projects").removeClass("active");
        $("#datasets").removeClass("active");
        $("#home").addClass("active");
        });
$("#about").click(function () {
        $("#about").addClass("active");
        $("#work").removeClass("active");
        $("#projects").removeClass("active");
        $("#datasets").removeClass("active");
        $("#home").removeClass("active");
        });
$("#work").click(function () {
        $("#work").addClass("active");
        $("#about").removeClass("active");
        $("#projects").removeClass("active");
        $("#datasets").removeClass("active");
        $("#home").removeClass("active");
        });
$("#projects").click(function () {
        $("#projects").addClass("active");
        $("#work").removeClass("active");
        $("#about").removeClass("active");
        $("#datasets").removeClass("active");
        $("#home").removeClass("active");
        });
$("#datasets").click(function () {
        $("#datasets").addClass("active");
        $("#work").removeClass("active");
        $("#projects").removeClass("active");
        $("#about").removeClass("active");
        $("#home").removeClass("active");
        });

$("#introduction").click(function () {
        $("#introduction").addClass("active");
        $("#juggling").removeClass("active");
        $("#cv").removeClass("active");
        });
$("#juggling").click(function () {
        $("#juggling").addClass("active");
        $("#introduction").removeClass("active");
        $("#cv").removeClass("active");
        });
$("#cv").click(function () {
        $("#cv").addClass("active");
        $("#introduction").removeClass("active");
        $("#juggling").removeClass("active");
        });

$("#papers").click(function () {
        $("#papers").addClass("active");
        $("#talks").removeClass("active");
        $("#courses").removeClass("active");
        });
$("#talks").click(function () {
        $("#talks").addClass("active");
        $("#papers").removeClass("active");
        $("#courses").removeClass("active");
        });
$("#courses").click(function () {
        $("#courses").addClass("active");
        $("#talks").removeClass("active");
        $("#papers").removeClass("active");
        });
