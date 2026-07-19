from .. import *
from ..words import random_phrase


def update_userlist():
  turbo.push(turbo.update(
    render_template("userlist.html",), "userlist"))
  
def refresh(user=None):
  run_script("location.reload();", user)



@app.route("/admin/new-user", methods=["POST"])
@superadmin
def new_user():
  new_user = request.args.get("name")
  if new_user is None:
    new_user = random_phrase(DB.users)
  if new_user is None:
    abort(500)
  DB.users[new_user] = {"status": 0, "admin": 0}
  update_userlist()
  return new_user


@app.route("/admin/new-admin", methods=["POST"])
@superadmin
def new_admin():
  new_user = request.args.get("name")
  if new_user is None:
    new_user = random_phrase(DB.users)
  if new_user is None:
    abort(500)
  DB.users[new_user] = {"status": 0, "admin": 1}
  update_userlist()
  return new_user


@app.route("/admin/user-status", methods=["POST"])
@admin
def user_status():
  data = request.get_json()
  user = data["user"]
  status = data["status"]
  if user not in DB.users or status not in [0, 1, 2, 3]:
    abort(400)

  if status == 0:
    if not superadmin():
      abort(401)
    DB.users[user]["status"] = 0
    update_userlist()
    run_script("logout()", user)
    return "ok"

  DB.users[user]["status"] = status
  if turbo.can_push(to=user):
    turbo.push(
      turbo.update(
        render_template("active_user.html", user=user),
        "active-user"
      ),
      to=user
    )
  update_userlist()
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
  update_userlist()
  return "ok"


@app.route("/admin/delete-user", methods=["POST"])
@superadmin
def delete_user():
  user = request.get_json()
  if user not in DB.users or admin_lvl(user) == 2:
    abort(400)
  del DB.users[user]
  refresh(user)
  update_userlist()
  return "ok"


@app.route("/admin/admin-status", methods=["POST"])
@superadmin
def admin_status():
  data = request.get_json()
  user = data["user"]
  status = data["status"]
  if user not in DB.users \
    or admin_lvl(user) == 2 \
    or status not in [0, 1]:
    abort(400)
  DB.users[user]["admin"] = status
  refresh(user)
  update_userlist()
  return "ok"


@app.route("/admin/run-script", methods=["POST"])
@superadmin
def force_run_script():
  data = request.get_json()
  user = data["user"]
  script = data["script"]
  run_script(script, user)
  return "ok"


@app.route("/admin/update-message", methods=["POST"])
@superadmin
def update_message():
  data = request.get_json()
  if DB.mode != "election":
    DB.mode = data.get("mode", "nothing")
  DB.message = data["message"]
  turbo.push(turbo.update(render_template("message.html"), "live-message"))
  return "ok"


@app.route("/admin/logout")
@superadmin
def admin_logout():
  user = get_user()
  DB.users[user]["status"] = 0
  session.pop("user")
  return "ok"