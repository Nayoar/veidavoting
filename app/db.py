import json
import os

db = None

def load():
  with open(os.path.dirname(os.path.realpath(__file__)) + "\\db.json") as dbfile:
    global db
    db = json.load(dbfile)

def save():
  with open(os.path.dirname(os.path.realpath(__file__)) + "\\db.json", "w") as dbfile:
    json.dump(db, dbfile, indent=2)