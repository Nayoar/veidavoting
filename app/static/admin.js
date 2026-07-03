const sendUpdate = (data, outID) => {
  fetch("/admin/update",
    {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    }
  )
  .then(r => {
    let out = document.getElementById(outID);
    if (out !== null) {
      if (r.status == 200) {
        out.innerHTML = "Updated!";
      } else {out.innerHTML = "Error :("}
      setTimeout(() => out.innerHTML = "", 1500);
    }
  })
}

const newUser = () => {
  fetch("/admin/new-user",
    {method: "POST"}
  )
  .then(r => r.text())
  .then(t => $("#new-user").html(t))
}

const activateUser = () => {
  sendUpdate({
    activate: $("#toggle-user").val()
  }, "confirm-toggle");
}

const deactivateUser = () => {
  sendUpdate({
    deactivate: $("#toggle-user").val()
  }, "confirm-toggle");
}

const setNothingMessage = () => {
  sendUpdate({
    mode: "none",
    message: $("#message").val()
  }, "message-confirm");
}

const setMotion = () => {
  sendUpdate({
    mode: "motion",
    message: $("#message").val()
  }, "message-confirm");
}

const presets = {
  "suspend-e4": "Suspend section E4 of the Constitution",
  "ratify-steering": "Ratify the steering committee",
  "ratify-chair": "Ratify the chairperson",
  "move-hanhallah": "Refer the current motion to the incoming Hanhallah",
  "amendment": "Approve the proposed amendment to the motion",
  "parts": "Vote on the current motion in separate parts",
  "move-to-vote": "Stop discussing the current motion and move immediately to voting on it",
  "vote-on-motion": "Pass the current motion"
}

const startVote = text => {
  let duration = parseInt($("#duration").val());
  fetch("/admin/start-vote",
    {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        text: text,
        duration: duration
      })
    }
  )
  .then(r => {
    let out = document.getElementById("vote-confirm");
    if (r.status != 200) out.innerHTML = "Error :(";
    setTimeout(() => out.innerHTML = "", 1500);
  })
}

const votePreset = e => {
  startVote(presets[e.id]);
}

const voteCustom = () => {
  startVote($("#custom-vote").val());
}

const endVote = a => {
  fetch(a ? "/admin/end-vote" : "/admin/cancel-vote",
    {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
      }
    }
  )
  .then(r => {
    let out = document.getElementById("vote-confirm");
    if (r.status != 200) out.innerHTML = "Error :(";
    setTimeout(() => out.innerHTML = "", 1500);
  })
}