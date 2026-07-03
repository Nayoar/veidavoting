from .. import *

def get_id():
  return session.get("user")

@turbo.user_id
def get_user_id():
  return get_id()
  
@app.route("/")
def index():

  if len(request.args) > 0:
    session["user"] = list(request.args.keys())[0]
  else:
    if "user" in session:
      session.pop("user")

  user = get_id()
  if user in db.db["users"] and db.db["users"][user] is None:
    db.db["users"][user] = True
    db.save()
  return render_template(
    "index.html",
    user = user if user in db.db["users"] else None,
    invalid = user is not None and user not in db.db["users"]
  )


@app.route("/display")
def display():
  return render_template("index.html", display=True)


@app.route("/", methods=["POST"])
def post_vote():

  if len(request.args) > 0:
    user = list(request.args.keys())[0]
  else:
    abort(401)
  if user not in db.db["users"] or not db.db["users"]:
    abort(401)

  if user in db.db["votes"][-1]["votes"]:
    abort(400)
  if now() > db.db["votes"][-1]["end"] + 2000:
    abort(400)

  choice = request.get_json()
  if choice not in ["Yes", "No", "Abstain"]:
    abort(400)

  db.db["votes"][-1]["votes"][user] = choice

  return "ok"