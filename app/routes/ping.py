from .. import *

@app.route("/healthz")
def healthz():
  return "ok", 200