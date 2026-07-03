const unspace = e => e.value = e.value.replace(" ", "-");

const login = () => window.location.href = "?" + $("#secret-code").val();

const vote = e => {
  if ($(e).hasClass("selected")) {
    $(e).removeClass("selected");
  } else {
    $(".vote-button").removeClass("selected");
    $(e).addClass("selected");
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
  fetch(window.location.href,
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
      $("#vote-submitted > span").html(choice);
      $("#vote-submitted").show()
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
    let remaining = Math.floor((end - now) / 1000);
    $("#seconds").html(remaining);
    let angle = 360 * (end - now) / (end - start);
    $("#timer").css(
      "background-image",
      `conic-gradient(white 0deg, white ${angle}deg, transparent ${angle}deg)`
    );
  } else {
    $("#voting-interface").hide();
    $("#vote-over").show()
  }
}, 50);


// setInterval(() => {
//   fetch("/ping")
//   .then(r => r.json())
//   .then(j => {
//     console.log(j);
//     if (!j) window.location.reload();
//   })
// }, 10000)