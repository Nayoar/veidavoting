from .. import *


@app.route("/")
def index():

  user = get_user()
  if user is not None:
    if superadmin():
      return render_template("superadmin.html", user=user)
    return render_template(
      "index.html",
      user = user,
      admin = admin()
    )

  if len(request.args) > 0:
    user = list(request.args.keys())[0].lower().strip("-")
    if user in DB.users:
      if vote_status(user) == 0:
        session["user"] = user
        if superadmin():
          return render_template("superadmin.html", user=user)
        DB.users[user]["status"] = 3
        return render_template(
          "index.html",
          user = user,
          admin = admin()
        )
      else:
        return render_template(
          "index.html",
          user = None,
          error = "already"
        ), 403
    else:
      return render_template(
        "index.html",
        user = None,
        error = "invalid"
      ), 401
    
  return render_template("index.html", user=None)


@app.route("/display")
def display():
  return render_template("index.html", display=True)


@app.route("/", methods=["POST"])
def post_vote():

  user = get_user()
  if vote_status(user) != 3:
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


@app.route("/favicon.ico")
def favicon():
  return redirect("https://www.bauk.org/wp-content/uploads/2023/03/cropped-SEMEL-TRANSPARENT-Sq-32x32.png")