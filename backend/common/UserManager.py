from mongo import mongo


def removeSensitiveInformation(x):
  if "passwordHash" in x:
    del x["passwordHash"]
  if x["accountType"] == "user":
    del x["apiKey"]
  return x


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

  @staticmethod
  def getUsers():
    return list(map(removeSensitiveInformation, list(mongo.users().find())))
