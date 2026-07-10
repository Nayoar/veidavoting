from .. import *
from ..words import random_phrase


@app.route("/admin-login")
def admin_login_page():
  return render_template("admin_login.html")


@app.route("/superadmin-logout")
@superadmin
def superadmin_logout():
  session["admin"] = "1"
  return "ok"


@app.route("/admin-logout")
def admin_logout():
  session["admin"] = "0"
  return "ok"


@app.route("/admin-login", methods=["POST"])
def admin_login():
  if request.form.get("password") == DB.admin_pw:
    session["admin"] = "1"
    return redirect("/", code=303)
  elif request.form.get("password") == DB.superadmin_pw:
    session["admin"] = "2"
    return redirect("/admin", code=303)
  else:
    return render_template("admin_login.html")


@app.route("/admin")
@admin
def admin_home():
  if superadmin():
    return render_template("superadmin.html")
  return render_template("useradmin.html")


@app.route("/admin", methods=["POST"])
@superadmin
def admin_post():
  return redirect("/?admin", code=307)


@app.route("/admin/new-user", methods=["POST"])
@admin
def new_user():
  new_user = random_phrase(DB.users)
  if new_user is None:
    abort(500)
  DB.users[new_user] = None
  return new_user


@app.route("/admin/activate-user", methods=["POST"])
@superadmin
def activate_user():
  user = request.get_json()
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
  return "ok"


@app.route("/admin/deactivate-user", methods=["POST"])
@admin
def deactivate_user():
  user = request.get_json()
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


@app.route("/admin/suspend-user", methods=["POST"])
@admin
def suspend_user():
  user = request.get_json()
  if user not in DB.users or user == "admin":
    abort(400)
  DB.users[user] = 0
  if turbo.can_push(to=user):
    turbo.push(
      turbo.update(
        render_template("active_user.html", user=user),
        "active-user"
      ),
      to=user
    )
  return "ok"


@app.route("/admin/unsuspend", methods=["POST"])
@superadmin
def unsuspend():
  for user in DB.users:
    if DB.users[user] == 0:
      DB.users[user] = True
      if turbo.can_push(to=user):
        turbo.push(
          turbo.update(
            render_template("active_user.html", user=user),
            "active-user"
          ),
          to=user
        )
  return "ok"


@app.route("/admin/update-message", methods=["POST"])
@superadmin
def update_message():
  data = request.get_json()
  DB.mode = data.get("mode", "nothing")
  DB.message = data["message"]
  turbo.push(turbo.update(render_template("message.html"), "live-message"))
  return "ok"