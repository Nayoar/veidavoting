import threading
import time
from .. import *


@app.route("/admin/start-vote", methods=["POST"])
def start_vote():

  if "admin" not in session:
    abort(401)

  if db.db["vote_active"]:
    abort(400)

  data = request.get_json()

  start = now()
  duration = data.get("duration", 20)

  db.db["votes"].append({
    "start": start,
    "end": start + duration * 1000,
    "message": db.db["message"],
    "vote_text": data.get("text", ""),
    "votes": {}
  })
  db.db["vote_active"] = True
  db.save()
  turbo.push(turbo.update(
      render_template("vote.html",), "live-vote"))
  threading.Thread(
    target=show_results,
    args=(duration,)
  ).start()
  return "ok"


def show_results(duration):
  time.sleep(duration + 2)
  db.save()
  with app.app_context():
    turbo.push(turbo.update(
      render_template("vote.html",), "live-vote"))


@app.route("/admin/end-vote", methods=["POST"])
def end_vote():

  if "admin" not in session:
    abort(401)

  if not db.db["vote_active"]:
    abort(400)

  end = now()
  if db.db["votes"][-1]["end"] > end:
    db.db["votes"][-1]["end"] = end
  db.save()
  turbo.push(turbo.update(
      render_template("vote.html",), "live-vote"))
  
  return "ok"


@app.route("/admin/cancel-vote", methods=["POST"])
def cancel_vote():

  if "admin" not in session:
    abort(401)

  if not db.db["vote_active"]:
    abort(400)

  end = now()
  if db.db["votes"][-1]["end"] > end:
    db.db["votes"][-1]["end"] = end
  db.db["vote_active"] = False
  db.save()
  turbo.push(turbo.update(
      render_template("vote.html",), "live-vote"))
  
  return "ok"