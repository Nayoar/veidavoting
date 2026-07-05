import os
import pymongo
import threading
import time

client = pymongo.MongoClient(os.getenv("DB")).veidavoting

class Database(dict):

  def __init__(self, synctime=2):
    super().__init__(**client.data.find_one({"_id": 0}))
    del self["_id"]
    threading.Thread(target=self.__synctimer, args=(synctime,)).start()

  def __getattr__(self, name):
    return self[name]
  
  def __setattr__(self, name, value):
    self[name] = value

  def sync(self):
    remote_old = client.data.find_one({"_id": 0})
    remote_new = client.data.find_one({"_id": 1})
    new = {}
    for k in remote_new:
      if k == "_id":
        continue
      if k not in remote_old or remote_old[k] != remote_new[k]:
        new[k] = remote_new[k]
        self[k] = remote_new[k]
      else:
        new[k] = self[k]
    client.data.update_many({}, {"$set": new})

  def __synctimer(self, synctime):
    while True:
      time.sleep(synctime)
      self.sync()

DB = Database()