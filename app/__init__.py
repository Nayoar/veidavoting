from datetime import datetime
from flask import abort, Flask, jsonify, redirect, render_template, request, session
import os
import requests
from turbo_flask import Turbo
from werkzeug.middleware.proxy_fix import ProxyFix

from .db import DB

now = lambda: int(datetime.now().timestamp() * 1000)

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
turbo = Turbo(app)
app.secret_key = os.getenv("SECRET_KEY")
app.config["PREFERRED_URL_SCHEME"] = "https"
app.config["SESSION_COOKIE_SECURE"] = True


@app.context_processor
def inject_db():
  
  context = {
    **DB,
    "now": now()
  }

  if len(DB.votes) > 0:
    votes = list(DB.votes[-1]["votes"].values())
    context["yes"] = votes.count("Yes")
    context["no"] = votes.count("No")
    context["abstain"] = votes.count("Abstain")
    context["total"] = len(votes)
    context["total_voters"] = list(DB.users.values()).count(True)

  return context


@app.before_request
def ip_info():
  ip = request.headers.get("CF-Connecting-IP")
  r = requests.get(f"https://api.ipinfo.io/lite/{ip}?token=ab6193ddc8b6b8").json()
  try:
    print(r["ip"], "|", r["as_name"], "|", r["country"])
  except:
    pass


def get_user():
  user = session.get("user")
  if user is None or user not in DB.users:
    return None
  return user

@turbo.user_id
def turbo_get_user():
  return session.get("user")

def admin_lvl(user):
  return DB.users[user]["admin"] if user is not None else 0

def vote_status(user):
  return DB.users[user]["status"] if user is not None else 0


def admin(func=None):
  if func is None:
    user = get_user()
    return admin_lvl(user) != 0
  def wrapper(*args, **kwargs):
    user = get_user()
    if admin_lvl(user) == 0:
      return abort(401)
    return func(*args, **kwargs)
  wrapper.__name__ = func.__name__
  return wrapper
  
def superadmin(func=None):
  if func is None:
    user = get_user()
    return admin_lvl(user) == 2
  def wrapper(*args, **kwargs):
    user = get_user()
    if admin_lvl(user) != 2:
      return abort(401)
    return func(*args, **kwargs)
  wrapper.__name__ = func.__name__
  return wrapper
  

from . import routes