$(document).ready(function (){

  var LHSoffers = [];
  var RHSoffers = [];


  //make draggable elements draggable
  $(".draggable").draggable({
    containment: "window",
    cursor: "crosshair",
    revert: "invalid",
    scroll: false,
    stop: function (event, ui) {
        if ($(this).hasClass("tsh")) {
            $(this).attr("style", "");

        }
    },
    drag: function (event, ui) {
        var offset = $(this).offset();
        var xPos = offset.left;
        var yPos = offset.top;
        var shw_xy = 'x: ' + xPos + 'y: ' + yPos;
        console.log(shw_xy);
    },
    help: "clone"
});

//make RHSoffer droppabe
$("#RHSoffer").droppable({
    accept: ".draggable",
    drop: function (event, ui) {
        $(this).removeClass("border").removeClass("over");
        var dropped = ui.draggable;
        var droppedOn = $(this);
        RHSoffers.push(dropped.text());

        $(dropped).detach().css({
                        top: 0,
                        left: 0
                    }).appendTo(droppedOn);
    },
    over: function (event, elem) {
        $(this).addClass("over");
        $(this).removeClass("img_added");

        var $this = $(this);

        //console.log("over");

    },
    activate: function (event, elem) {

    }
});
//make theiritems droppable
$("#RHSitems").droppable({
    accept: ".draggable",
    drop: function (event, ui) {
        $(this).removeClass("border").removeClass("over");
        var dropped = ui.draggable;
        var droppedOn = $(this);
        RHSoffers.push(dropped.text());

        $(dropped).detach().css({
                        top: 0,
                        left: 0
                    }).appendTo(droppedOn);
    },
    over: function (event, elem) {
        $(this).addClass("over");
        $(this).removeClass("img_added");

        var $this = $(this);

        //console.log("over");

    },
    activate: function (event, elem) {

    }
});

$("#LHSoffer").droppable({
    accept: ".draggable",
    activeClass: "myhighlight",
    drop: function (event, ui) {
      $(this).removeClass("border").removeClass("over");
                    //$(this).addClass("over");
                    var dropped = ui.draggable;
                    var droppedOn = $(this);
                    $(dropped).detach().css({
                        top: 0,
                        left: 0
                    }).appendTo(droppedOn); // add the item to the div element visually
    },
    over: function (event, elem) {

        //$(this).addClass("over");
        //$(this).removeClass("img_added");

        //var $this = $(this);

        //console.log("over");

    },
    activate: function (event, elem) {

    }
});

$("#submitOffer").on("click", function (){
  // we want to make an AJAX post request, sending the contents of the RHSoffers and LHSoffers
  alert(RHSoffers);
});

});
