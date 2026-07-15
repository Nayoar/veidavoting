const sendUpdate = (url, data, outID) => {
  fetch(url,
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

const newUser = name => {
  fetch("/admin/new-user" + (name !== undefined ? "?name="+name : ""),
    {method: "POST"}
  )
  .then(r => r.text())
  .then(t => $("#toggle-user").val(t))
}

const newAdmin = name => {
  fetch("/admin/new-admin" + (name !== undefined ? "?name="+name : ""),
    {method: "POST"}
  )
  .then(r => r.text())
  .then(t => $("#toggle-user").val(t))
}

const userStatus = s => sendUpdate(
  "/admin/user-status",
  {
    user: $("#toggle-user").val(),
    status: s
  },
  "confirm-toggle"
);

const unsuspend = () => sendUpdate(
  "/admin/unsuspend",
  {},
  "confirm-toggle"
);

const deleteUser = () => {
  sendUpdate(
    "/admin/delete-user",
    $("#toggle-user").val(),
    "confirm-toggle"
  );
  $("#toggle-user").val("");
}

const adminStatus = s => sendUpdate(
  "/admin/admin-status",
  {
    user: $("#toggle-user").val(),
    status: s
  },
  "confirm-toggle"
)

const runScript = script => sendUpdate(
  "/admin/run-script",
  {
    user: $("#toggle-user").val(),
    script: script
  },
  "confirm-toggle"
)

const setMessage = m => sendUpdate(
  "/admin/update-message",
  {
    mode: m,
    message: $("#edit-message").val()
  },
  "message-confirm"
);

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

const votePreset = e => startVote(presets[e.id]);

const voteCustom = () => startVote($("#custom-vote").val());

const extendVote = () => {
  let duration = parseInt($("#duration").val());
  fetch("/admin/extend-vote",
    {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify(duration)
    }
  )
  .then(r => {
    let out = document.getElementById("vote-confirm");
    if (r.status != 200) out.innerHTML = "Error :(";
    setTimeout(() => out.innerHTML = "", 1500);
  })
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

const logout = () => {
  fetch("/admin/logout")
  .then(r => location.href = "/");
}