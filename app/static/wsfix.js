let wsDown = false;

async function checkWS() {
  try {
    if (!wsDown) {
      const response = await fetch(
        "/ws-check",
        {cache: "no-store"}
      );
      if (!response.ok) {
        wsDown = true;
      }
    } else {
      const response = await fetch(
        "/healthz",
        {cache: "no-store"}
      );
      if (response.ok) {
        if (!ADMIN) location.reload();
        else $("#connection-lost").show();
      }
    }
  } catch {
    wsDown = true;
  }
}

setInterval(checkWS, 5000);