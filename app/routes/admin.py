from .. import *
from ..words import random_phrase


@app.route("/admin/new-user", methods=["POST"])
@admin
def new_user():
  new_user = random_phrase(DB.users)
  if new_user is None:
    abort(500)
  DB.users[new_user] = {"status": 0, "admin": 0}
  return new_user


@app.route("/admin/activate-user", methods=["POST"])
@admin
def activate_user():
  user = request.get_json()
  if user not in DB.users:
    abort(400)
  DB.users[user]["status"] = 3
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
  if user not in DB.users:
    abort(400)
  DB.users[user]["status"] = 1
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
  if user not in DB.users:
    abort(400)
  DB.users[user] = 2
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
    if DB.users[user]["status"] == 2:
      DB.users[user]["status"] = 3
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


@app.route("/admin/logout")
@superadmin
def admin_logout():
  session.pop("user")
  return "ok"