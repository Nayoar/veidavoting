from datetime import datetime
from flask import abort, Flask, jsonify, redirect, render_template, request, session
import os
from turbo_flask import Turbo

from . import db
db.load()

now = lambda: int(datetime.now().timestamp() * 1000)

app = Flask(__name__)
turbo = Turbo(app)
app.secret_key = os.getenv("SECRET_KEY")

from . import routes

@app.context_processor
def inject_db():
  
  context = {**db.db, "now": now()}

  if len(db.db["votes"]) > 0:
    votes = list(db.db["votes"][-1]["votes"].values())
    context["yes"] = votes.count("Yes")
    context["no"] = votes.count("No")
    context["abstain"] = votes.count("Abstain")
    context["total"] = len(votes)
    context["total_voters"] = list(db.db["users"].values()).count(True)

  return context