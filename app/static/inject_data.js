const injectData = () => {
  let user = $("#user-data").attr("data-user");
  let status = $("#user-data").attr("data-status");

  if (status == 0) {
    $(".not-yet-voted").hide();
    $("#no-vote").show();
    return;
  }

  let mode = $("#mode").attr("data-mode");

  if (mode == "vote") {

    let voted = $("#user-data").attr("data-voted") == "1";
    let choice = $("#user-data").attr("data-choice");

    if (voted) {

      $("#voting-interface").show();
      $("#status-1, #status-2").hide();
      $(".not-yet-voted").hide();
      $("#vote-choice").html(choice);
      $("#vote-submitted").show();

    } else {

      if (status == 1) {
        $(".not-yet-voted").hide();
        $("#status-1").show();
        $("#status-2").hide();
      } else if (status == 2) {
        $(".not-yet-voted").hide();
        $("#status-1").hide();
        $("#status-2").show();
      } else {
        $(".not-yet-voted").show();
        $("#status-1, #status-2").hide();
      }

    }
  } else if (mode == "election") {

    let voted = $("#user-data").attr("data-elected") == "1";

    const RON = "<i>Reopen nominations</i>";

    if (voted) {

      $("#election-interface, #voted").show();
      $("#status-non3, .not-yet-voted").hide();
      $("#election-submitted").html("");

      let choice = $("#user-data .selected-candidate")
        .map(function(){
          return $(this).attr("data-candidate")
        }).toArray();
      
      choice.forEach((cand, i) => {
        let n = $(`<span>${i+1}</span>`).addClass("number");
        let c = $("<span></span>").addClass("candidate-name");
        if (cand == "RON") c.html(RON);
        else c.html(cand);
        let d = $("<div></div>")
          .addClass("candidate")
          .append(n, c);
        $("#election-submitted").append(d);
      })
      return;

    } else if (status == 1 || status == 2) {
      $(".not-yet-voted").hide();
      $("#status-non3, #no-vote").show();
      return;
    }

    $("#available-candidates, #selected-candidates").html("");
    
    $("#user-data .unselected-candidate")
    .map(function(){
      return $(this).attr("data-candidate")
    }).each((i, cand) => {
      $("#candidate-template > div")
        .clone()
        .attr("data-candidate", cand)
        .find(".candidate-name").html(cand == "RON" ? RON : cand)
        .parent().appendTo("#available-candidates");
    });

    $("#user-data .selected-candidate")
    .map(function(){
      return $(this).attr("data-candidate")
    }).each((i, cand) => {
      $("#candidate-template > div")
        .clone()
        .attr("data-candidate", cand)
        .find(".candidate-name").html(cand == "RON" ? RON : cand)
        .prev().html(i+1)
        .parent().appendTo("#selected-candidates");
    });

    if ($("#selected-candidates .candidate").length >= $("#mode").attr("data-positions")) {
      $("#available-candidates").addClass("max-reached");
    }

    $(".not-yet-voted").show();
    $("#status-non3, #no-vote").hide();

  }
}