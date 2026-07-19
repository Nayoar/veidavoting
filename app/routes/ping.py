from .. import *

@app.route("/healthz")
def healthz():
  return "ok", 200

@app.route("/ws-check")
def ws_check():
  user = turbo_get_user()
  if user is None:
    abort(400)
  if turbo.can_push(to=user):
    return "ok", 200
  else:
    return "no", 400