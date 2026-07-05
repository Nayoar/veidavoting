// AI-WRITTEN

window.__turboSocketDead = false;

const NativeWebSocket = window.WebSocket;

window.WebSocket = function(url, protocols) {
  const socket = protocols
    ? new NativeWebSocket(url, protocols)
    : new NativeWebSocket(url);

  if (String(url).includes("/turbo-stream")) {
    socket.addEventListener("close", () => {
      console.warn("Turbo WebSocket closed");
      window.__turboSocketDead = true;
    });

    socket.addEventListener("error", () => {
      console.warn("Turbo WebSocket error");
      window.__turboSocketDead = true;
    });
  }

  return socket;
};

window.WebSocket.prototype = NativeWebSocket.prototype;
window.WebSocket.CONNECTING = NativeWebSocket.CONNECTING;
window.WebSocket.OPEN = NativeWebSocket.OPEN;
window.WebSocket.CLOSING = NativeWebSocket.CLOSING;
window.WebSocket.CLOSED = NativeWebSocket.CLOSED;