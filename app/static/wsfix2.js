// AI-WRITTEN

async function reloadWhenServerReturns() {
  if (!window.__turboSocketDead) {
    return;
  }

  try {
    const response = await fetch("/healthz", {
      cache: "no-store"
    });

    if (response.ok) {
      console.warn("Server is back; reloading to recreate Turbo WebSocket");
      window.location.reload();
    }
  } catch {
    // Server still unavailable. Try again on the next interval.
  }
}

setInterval(reloadWhenServerReturns, 3000);