import threading
import time
from .. import *

def push_vote():
  turbo.push([
    turbo.update(render_template("vote.html",), "live-vote"),
    turbo.update("", "live-election")
  ])


def show_results():
  while True:
    time.sleep(0.1)
    if len(DB.votes) == 0 or not DB.vote_active:
      return
    if now() > DB.votes[-1]["end"] + 2000:
      break
  with app.app_context():
    push_vote()    


@app.route("/admin/start-vote", methods=["POST"])
@superadmin
def start_vote():

  if DB.mode == "election":
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
  push_vote()
  threading.Thread(target=show_results).start()
  return "ok"


@app.route("/admin/extend-vote", methods=["POST"])
@superadmin
def extend_vote():

  if DB.mode == "election" or not DB.vote_active:
    abort(400)

  data = request.get_json()
  DB.votes[-1]["end"] += data * 1000
  push_vote()
  return "ok"


@app.route("/admin/end-vote", methods=["POST"])
@superadmin
def end_vote():

  if DB.mode == "election" or not DB.vote_active:
    abort(400)

  end = now()
  if DB.votes[-1]["end"] > end:
    DB.votes[-1]["end"] = end
  push_vote()
  
  return "ok"


@app.route("/admin/cancel-vote", methods=["POST"])
@superadmin
def cancel_vote():

  if DB.mode == "election" or not DB.vote_active:
    abort(400)

  end = now()
  if DB.votes[-1]["end"] > end:
    DB.votes[-1]["end"] = end
  DB.vote_active = False
  push_vote()
  
  return "ok"


@app.route("/admin/clear-election", methods=["POST"])
@superadmin
def clear_election():

  if not (DB.mode == "election" and DB.elections[-1]["end"] <= now()):
    abort(400)

  DB.mode = "nothing"
  DB.vote_active = False
  push_vote()
  
  return "ok"