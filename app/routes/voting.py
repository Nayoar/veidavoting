import threading
import time
from .. import *


@app.route("/admin/start-vote", methods=["POST"])
def start_vote():

  if "admin" not in session:
    abort(401)

  if DB.vote_active:
    abort(400)

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
  threading.Thread(
    target=show_results,
    args=(duration,)
  ).start()
  return "ok"


def show_results(duration):
  time.sleep(duration + 2)
  with app.app_context():
    turbo.push(turbo.update(
      render_template("vote.html",), "live-vote"))


@app.route("/admin/end-vote", methods=["POST"])
def end_vote():

  if "admin" not in session:
    abort(401)

  if not DB.vote_active:
    abort(400)

  end = now()
  if DB.votes[-1]["end"] > end:
    DB.votes[-1]["end"] = end
  turbo.push(turbo.update(
      render_template("vote.html",), "live-vote"))
  
  return "ok"


@app.route("/admin/cancel-vote", methods=["POST"])
def cancel_vote():

  if "admin" not in session:
    abort(401)

  if not DB.vote_active:
    abort(400)

  end = now()
  if DB.votes[-1]["end"] > end:
    DB.votes[-1]["end"] = end
  DB.vote_active = False
  turbo.push(turbo.update(
      render_template("vote.html",), "live-vote"))
  
  return "ok"