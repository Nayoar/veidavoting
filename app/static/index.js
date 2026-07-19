const unspace = e => $(e).val($(e).val().replace(" ", "-"))

$("#secret-code").on("keyup", e => {
  if (e.key === "Enter" || e.keyCode === 13) login();
  else unspace($("#secret-code"));
})

const login = () => {
  let username = $("#secret-code").val();
  if (username == "admin") location.href = "/admin-login";
  else location.href = "?" + username;
}

const logout = () => {
  fetch("/logout")
  .then(r => {
    if (r.status == 200) location.href = "/";
  })
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




const savePos = elmnts => elmnts.map(el => el.getBoundingClientRect());

const slide = (elmnts, oldPos, time) => {
  elmnts.forEach((el, i) => {
    const newPos = el.getBoundingClientRect();
    const dY = oldPos[i].top - newPos.top;
    el.animate(
      [
        { transform: `translateY(${dY}px)` },
        { transform: "translateY(0)" }
      ], {
        duration: time,
        easing: "ease"
      }
    )
  })
}

const renumber = () => {
  $("#selected-candidates .candidate").each((i, el) => {
    $(el).children(".number").html(i + 1);
  })
}

const selectChoice = cand => {
  if ($("#available-candidates").hasClass("max-reached")) return;
  const elmnts = [$(cand)[0]];
  const oldPos = savePos(elmnts);
  $("#selected-candidates").append($(cand));
  renumber();
  submitElection(false);
  if ($("#selected-candidates .candidate").length == $("#election-interface").attr("data-positions")) {
    $("#available-candidates").addClass("max-reached");
  }
  slide(elmnts, oldPos, 500);
}

const moveUp = cand => {
  let prev = $(cand).prev();
  const elmnts = [$(cand)[0], prev[0]];
  const oldPos = savePos(elmnts);
  $(cand).detach().insertBefore(prev);
  renumber();
  submitElection(false);
  slide(elmnts, oldPos, 300);
}

const moveDown = cand => {
  let next = $(cand).next();
  const elmnts = [$(cand)[0], next[0]];
  const oldPos = savePos(elmnts);
  $(cand).detach().insertAfter(next);
  renumber();
  submitElection(false);
  slide(elmnts, oldPos, 300);
}

const removeChoice = cand => {
  const elmnts = [$(cand)[0]];
  const oldPos = savePos(elmnts);
  $("#available-candidates").append($(cand));
  renumber();
  submitElection(false);
  if ($("#selected-candidates .candidate").length == $("#election-interface").attr("data-positions") - 1) {
    $("#available-candidates").removeClass("max-reached");
  }
  slide(elmnts, oldPos, 500);
}

const submitElection = submit => {
  let unselected = $("#available-candidates .candidate")
    .map(function(){
      return $(this).attr("data-candidate")
    }).toArray();
  let selected = $("#selected-candidates .candidate")
    .map(function(){
      return $(this).attr("data-candidate")
    }).toArray();
  fetch("/submit-election",
    {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        selected: selected,
        unselected: unselected,
        submit: submit
      })
    }
  ).then(r => {
    if (r.status != 200) {
      $("#save-error").html("Error :(");
      setTimeout(() => $("#save-error").html(""), 1500);
    } else if (submit) location.reload();
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


setInterval(() => {
  let currentElection = $("#election-timer");
  let start = parseInt($("#election-start").html());
  let end = parseInt($("#election-end").html());
  let now = Date.now();
  if (now < end) {
    let totalSeconds = Math.floor((end - now) / 1000);
    let seconds = totalSeconds % 60;
    let secondsStr = String(seconds).padStart(2, "0");
    let minutes = Math.floor(totalSeconds / 60);
    $("#election-timer > span").html(`${minutes}:${secondsStr}`);
    if (end < now + 15000) {
      $("#submit-election").addClass("urgent");
    } else $("#submit-election").removeClass("urgent");
  } else {
    $("#election-interface").hide();
    $("#election-over").show()
  }
}, 200);