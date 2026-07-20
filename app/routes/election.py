import random
from .. import *

def shuffle_candidates(candidates):
  if "RON" in candidates:
    candidates.remove("RON")
    random.shuffle(candidates)
    candidates.append("RON")
  else:
    random.shuffle(candidates)
  return candidates

app.jinja_env.filters["shuffle"] = shuffle_candidates

def push_election(new=False):
  turbo.push(turbo.update(
    render_template("election.html", new=new),
    "live-vote"
  ))

@app.route("/submit-election", methods=["POST"])
def save_election_choice():
  
  user = get_user()
  if user is None:
    abort(401)

  if not (DB.mode == "election" and DB.vote_active):
    abort(400)

  data = request.get_json()
  selected = data.get("selected", [])
  unselected = data.get("unselected", [])
  submit = data.get("submit", False)

  if user in DB.elections[-1]["votes"]:
      abort(403)

  if (submit and len(selected) == 0) \
    or len(selected) > DB.elections[-1]["positions"] \
    or sorted(DB.elections[-1]["candidates"]) != sorted(selected + unselected):
    abort(400)

  if submit:
    if user in DB.elections[-1]["provisional"]:
      del DB.elections[-1]["provisional"][user]
    DB.elections[-1]["votes"][user] = selected

  else:
    DB.elections[-1]["provisional"][user] = {
      "selected": data["selected"],
      "unselected": data["unselected"]
    }

  return "ok"


@app.route("/admin/start-election", methods=["POST"])
@superadmin
def start_election():

  data = request.get_json()

  start = now()
  duration = data.get("duration", 20)
  candidates = data.get("candidates")
  if "RON" not in candidates:
    candidates.append("RON")

  DB.mode = "election"
  DB.elections.append({
    "start": start,
    "end": start + duration * 1000,
    "role": data.get("role", "[unspecified]"),
    "positions": data.get("positions", 1),
    "candidates": candidates,
    "provisional": {},
    "votes": {}
  })
  DB.vote_active = True
  push_election(True)
  return "ok"


@app.route("/admin/extend-election", methods=["POST"])
@superadmin
def extend_election():

  if not (DB.mode == "election" and DB.vote_active):
    abort(400)

  data = request.get_json()
  DB.elections[-1]["end"] += data * 1000
  push_election()
  return "ok"


@app.route("/admin/end-election", methods=["POST"])
@superadmin
def end_election():

  if not (DB.mode == "election" and DB.vote_active):
    abort(400)

  end = now()
  if DB.elections[-1]["end"] > end:
    DB.elections[-1]["end"] = end
  push_election()
  return "ok"