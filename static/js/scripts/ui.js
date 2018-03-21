// this is where we should put in the jQuery and jQuery UI for offer notifications

$(document).ready(function(){
    // put jquery ui functionality here


    var $youritems = $("#youritems"), $theiritems = $("#theiritems"), $youroffer = $("#youroffer"), $theiroffer = $("#theiroffer");
    $( ".draggable" ).draggable({
      cancel: "a.ui-icon", // clicking an icon won't initiate dragging
      revert: "invalid", // when not dropped, the item will revert back to its initial position
      revertDuration:100,
      containment: "document",
      helper: "clone",
      cursor: "move"
    });

    // the following is for the haggle view functionality
    //////////////////////////////////////////////////////////
    // this makes your inventory accept the items you offered
    $("#youritems.droppable").droppable({
        accept:"#youroffer > .item-card",
        drop: function(event, ui){takeYourItemBack(ui.draggable);}
      }
    );
    // this makes the LHS of the offer table accept your items
    $("#youroffer.droppable").droppable(
      {
        accept:"#youritems > .item-card",
        drop: function(event, ui){offerYourItem(ui.draggable);}
      }
    );
    ///////////////////////////////////////////////////////
    // this makes their inventory accept offered items
    $("#theiritems.droppable").droppable(
      {
        accept:"#theiroffer > .item-card",
        drop: function(event, ui){takeTheirItemBack(ui.draggable);}
      }
    );
    // this makes the RHS of the offer table accept their items
    $("#theiroffer.droppable").droppable(
      {
        accept:"#theiritems > .item-card",
        drop: function(event, ui){offerTheirItem(ui.draggable);}
      }
    );
    /////////////////////////////////////////////////////////
    $(".item-tooltip").tooltip({track:true});

    function offerYourItem($item){
      alert("called");
      $item.fadeOut(function(){
        var next_icon = "<a href='#' title='Take this back' class='ui-icon ui-icon-refresh'></a>";
        var $list = $("ul", $youroffer).length ? $("ul", $youroffer) : $( "<ul id='youritems' class=' ui-helper-reset'/>" ).appendTo( $youroffer );
        $item.find( "a.ui-icon-arrow-2-e-w" ).remove();
        $item.append( next_icon ).appendTo( $list ).fadeIn(function() {
          $item.animate({ width: "48px" }).find( "img" ).animate({ height: "36px" });
        });
      })
    }
    function offerTheirItem($item){}
    function takeYourItemBack($item){
      $item.fadeOut(function(){

      });
    }
    function takeTheirItemBack($item){}
    function submitOffer(){
      var LHSoffer = []; // list to store the itemIDs of the items in the LHS of the offer table
      var RHSoffer = []; // list to store the itemIDs of the items in the RHS of the offer table
      $("#youritems").find("li").css("background-color","blue");
    }
    $("#submitOffer").on("click", submitOffer);


    $( "#youritems > li" ).on( "click", function( event ) {
      alert("alerted");
      var $item = $( this ), $target = $( event.target );
      if ( $target.is( "a" ) ) {
        offerYourItem( $item );
      } else if ( $target.is( "a.ui-icon-refresh" ) ) {
        takeYourItemBack( $item );
      }
      return false;
    });

    $( "#theiritems > li" ).on( "click", function( event ) {
      var $item = $( this ), $target = $( event.target );
      if ( $target.is( "a.ui-icon-arrow-2-e-w" ) ) {
        offerTheirItem( $item );
      } else if ( $target.is( "a.ui-icon-refresh" ) ) {
        takeTheirItemBack( $item );
      }
      return false;
    });

    /////////////////////////////////////////////////////////


  });
