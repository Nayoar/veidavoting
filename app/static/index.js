const unspace = e => e.val(e.val().replace(" ", "-"))

$("#secret-code").on("keyup", e => {
  if (e.key === "Enter" || e.keyCode === 13) login();
  else unspace($("#secret-code"));
})

const login = () => {
  let username = $("#secret-code").val();
  if (username == "admin") location.href = "/admin";
  else location.href = "?" + username;
}

const vote = e => {
  if ($(e).hasClass("selected")) {
    $(e).removeClass("selected");
  } else {
    $(".vote-button").removeClass("selected");
    $(e).addClass("selected");
    $([document.documentElement, document.body]).animate({
      scrollTop: $("#vote-warning").offset().top
    }, 500);
  }
}

const submitVote = () => {
  let selected = $(".selected")[0];
  if (selected === undefined) return;
  let choice = {
    "vote-yes": "Yes",
    "vote-no": "No",
    "abstain": "Abstain"
  }[selected.id];
  fetch(location.href,
    {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify(choice)
    }
  )
  .then(r => {
    if (r.status == 200) {
      $("#vote-buttons, #submit-vote, #vote-warning").hide();
      $("#vote-choice").html(choice);
      // $("#live-vote").css(`--${choice}`, "inline");
      $("#vote-submitted").show();
    } else {
      $("#error").show();
    }
  })
}

setInterval(() => {
  let currentVote = $("#vote");
  let start = currentVote.attr("data-start");
  let end = currentVote.attr("data-end");
  let now = Date.now();
  if (now < end) {
    $("#seconds").html(Math.floor((end - now) / 1000));
  } else {
    $("#voting-interface").hide();
    $("#vote-over").show()
  }
}, 200);