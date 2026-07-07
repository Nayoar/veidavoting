from .. import *
from ..words import random_phrase


@app.route("/admin", methods=["GET", "POST"])
def admin():

  if request.method == "POST":
    return redirect("/?admin", code=307)

  if "admin" not in session:
    return render_template("admin_login.html")
  
  return render_template("admin.html")


@app.route("/admin-login", methods=["POST"])
def admin_login():
  if request.form.get("password") == "p4ssw0rd":
    session["admin"] = "true"
  return redirect("/admin", code=303)


@app.route("/admin/update", methods=["POST"])
def update_message():

  if "admin" not in session:
    abort(401)

  data = request.get_json()
  
  if "message" in data:
    DB.mode = data.get("mode", "nothing")
    DB.message = data["message"]
    turbo.push(turbo.update(render_template("message.html"), "live-message"))

  if "activate" in data:
    user = data["activate"]
    if user not in DB.users or user == "admin":
      abort(400)
    DB.users[user] = True
    if turbo.can_push(to=user):
      turbo.push(
        turbo.update(
          render_template("active_user.html", user=user),
          "active-user"
        ),
        to=user
      )

  if "deactivate" in data:
    user = data["deactivate"]
    if user not in DB.users or user == "admin":
      abort(400)
    DB.users[user] = False
    if turbo.can_push(to=user):
      turbo.push(
        turbo.update(
          render_template("active_user.html", user=user),
          "active-user"
        ),
        to=user
      )

  return "ok"


@app.route("/admin/new-user", methods=["POST"])
def new_user():

  if "admin" not in session:
    abort(401)

  new_user = random_phrase(DB.users)
  if new_user is None:
    abort(500)
  
  DB.users[new_user] = None

  return new_user