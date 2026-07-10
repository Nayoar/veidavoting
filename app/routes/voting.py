import threading
import time
from .. import *


def show_results():
  while True:
    time.sleep(0.1)
    if len(DB.votes) == 0 or not DB.vote_active:
      return
    if now() > DB.votes[-1]["end"] + 2000:
      break
  with app.app_context():
    turbo.push(turbo.update(
      render_template("vote.html",), "live-vote"))


@app.route("/admin/start-vote", methods=["POST"])
@superadmin
def start_vote():

  data = request.get_json()

  start = now()
  duration = data.get("duration", 20)

  DB.votes.append({
    "start": start,
    "end": start + duration * 1000,
    "message": DB.message,
    "mode": DB.mode,
    "vote_text": data.get("text", ""),
    "votes": {}
  })
  DB.vote_active = True
  turbo.push(turbo.update(
    render_template("vote.html",), "live-vote"))
  threading.Thread(target=show_results).start()
  return "ok"


@app.route("/admin/extend-vote", methods=["POST"])
@superadmin
def extend_vote():

  if not DB.vote_active:
    abort(400)

  data = request.get_json()
  DB.votes[-1]["end"] += data * 1000
  turbo.push(turbo.update(
    render_template("vote.html",), "live-vote"))
  return "ok"


@app.route("/admin/end-vote", methods=["POST"])
@superadmin
def end_vote():

  if not DB.vote_active:
    abort(400)

  end = now()
  if DB.votes[-1]["end"] > end:
    DB.votes[-1]["end"] = end
  turbo.push(turbo.update(
    render_template("vote.html",), "live-vote"))
  
  return "ok"


@app.route("/admin/cancel-vote", methods=["POST"])
@superadmin
def cancel_vote():

  if not DB.vote_active:
    abort(400)

  end = now()
  if DB.votes[-1]["end"] > end:
    DB.votes[-1]["end"] = end
  DB.vote_active = False
  turbo.push(turbo.update(
    render_template("vote.html",), "live-vote"))
  
  return "ok"