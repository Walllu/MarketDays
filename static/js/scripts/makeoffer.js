$(document).ready(function (){


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
    /*drag: function (event, ui) {
        var offset = $(this).offset();
        var xPos = offset.left;
        var yPos = offset.top;
        var shw_xy = 'x: ' + xPos + 'y: ' + yPos;
        console.log(shw_xy);
    },*/
    help: "clone"
});

// A function that is used to make uniqe element arrays
function onlyUnique(value, index, self) {
    return self.indexOf(value) === index;
}

//make RHSoffer droppabe
$("#RHSoffer").droppable({
    accept: ".draggable",
    drop: function (event, ui) {
        $(this).removeClass("border").removeClass("over");
        var dropped = ui.draggable;
        var droppedOn = $(this);

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

//make theiritems droppable
$("#LHSitems").droppable({
    accept: ".draggable",
    drop: function (event, ui) {
        $(this).removeClass("border").removeClass("over");
        var dropped = ui.draggable;
        var droppedOn = $(this);


        $(dropped).detach().css({
                        top: 0,
                        left: 0
                    }).appendTo(droppedOn);
    },
    over: function (event, elem) {
        $(this).addClass("over");
        $(this).removeClass("img_added");

        var $this = $(this);

        console.log("over");

    },
    activate: function (event, elem) {

    }
});




// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});






$("#submitOffer").on("click", function (){
  // we want to make an AJAX post request, sending the contents of the RHSoffers and LHSoffers
  function listEach(list){
    dalist = []; // this list will hold all the itemID in the area we're interested in
    for(var i=0;i<list.length;i++){
      dalist.push(list[i].children.namedItem("hiddenID").innerHTML);
    }
    return dalist;
  }
  RHSoffers = $("#RHSoffer").find(".trading-card").get();
  LHSoffers = $("#LHSoffer").find(".trading-card").get();
  offerMessage = $("¤offer-message").children;
  alert(offerMessage);
  var RHSoffers = listEach(RHSoffers); // this holds the itemIDs of the RHSoffers
  var LHSoffers = listEach(LHSoffers);// this holds the itemIDs of the LHSoffers
  //we also need to extract the text in the message box

  var content = {LHS:LHSoffers, RHS:RHSoffers};
  //now we send the information via POST request
  $.ajax({
    type:'POST',
    url:'/market/api/makeoffer/',
    data: content,
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    success: function(ret) {
      alert("success");
    },
    error: function(ret) {
      alert("failure");
    }
  });

});

});
