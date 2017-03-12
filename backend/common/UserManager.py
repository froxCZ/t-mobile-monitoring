from mongo import mongo


class UserManager():
  @staticmethod
  def getUserByApiKey(apiKey):
    if apiKey is None:
      return None
    return mongo.users().find_one({"apiKey": apiKey})

  @staticmethod
  def getUserByName(username):
    if username is None:
      return None
    return mongo.users().find_one({"_id": username})
