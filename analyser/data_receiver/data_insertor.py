from datetime import timedelta

from mongo import mongo


class DataInsertor():
  def insertInputs(self, inputsList):
    """
    inserts inputsList into database.
    :param inputsList: list of objects containing date and input data information.
    :return:
    """
    coll = mongo.lobs()
    updates = _sumUpdates(list(map(_createInputUpdateDict, inputsList)))
    print("Inserted " + str(len(inputsList)) + " rows")
    for key, value in updates.items():
      coll.update({'_id': key}, value, upsert=True)

  def insertForwards(self, forwardsList):
    pass


def _createInputUpdateDict(row):
  date = row["date"]
  indexDate = date - timedelta(seconds=date.second)

  updatePath = "data." + row["lob"] + ".inputs."
  try:
    dataSize = int(row["dataSize"])
  except ValueError:
    print("ValueError: " + row["dataSize"])
    print(row)
    dataSize = 0
  update = {"$inc":
              {updatePath + row["neid"]: dataSize,
               updatePath + "sum": dataSize,
               updatePath + "updatesCnt": 1
               }
            }
  return (indexDate, update)


def _sumUpdates(updates):
  sums = {}
  for indexDate, update in updates:
    if indexDate not in sums:
      sums[indexDate] = update
    else:
      prevUpdate = sums[indexDate]
      for key, value in update["$inc"].items():
        if key in prevUpdate["$inc"]:
          prevUpdate["$inc"][key] += value
        else:
          prevUpdate["$inc"][key] = value

  return sums
