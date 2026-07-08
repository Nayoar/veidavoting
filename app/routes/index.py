from .. import *

def clean(user):
  return user.lower().strip("-")

def get_id():
  return session.get("user")

@turbo.user_id
def get_user_id():
  return get_id()
  
@app.route("/")
def index():

  if len(request.args) > 0:
    session["user"] = clean(list(request.args.keys())[0])
  else:
    if "user" in session:
      session.pop("user")

  user = get_id()
  if user == "admin":
    user = "congrats you found an easter egg"
  if user in DB.users and DB.users[user] is None:
    DB.users[user] = True
  invalid = user is not None and user not in DB.users
  return render_template(
    "index.html",
    user = user if user in DB.users else None,
    invalid = invalid
  ), 401 if invalid else 200


@app.route("/display")
def display():
  return render_template("index.html", display=True)


@app.route("/", methods=["POST"])
def post_vote():

  if len(request.args) > 0:
    user = clean(list(request.args.keys())[0])
  else:
    abort(401)
  if user not in DB.users \
    or not DB.users \
    or (user == "admin" and "admin" not in session):
    abort(401)

  if user in DB.votes[-1]["votes"]:
    abort(400)
  if now() > DB.votes[-1]["end"] + 2000:
    abort(400)

  choice = request.get_json()
  if choice not in ["Yes", "No", "Abstain"]:
    abort(400)

  DB.votes[-1]["votes"][user] = choice

  return "ok"