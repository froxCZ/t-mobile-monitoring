from datetime import timedelta

from mongo import mongo

"""
deprecated
"""
class DataInsertor():

  def __init__(self):
    super().__init__()

  def insertRows(self, rowList):
    coll = mongo.traffic()
    updates = _sumUpdates(list(map(_createRowUpdateDict, rowList)))
    print("Inserted " + str(len(rowList)) + " rows")
    for key, value in updates.items():
      coll.update({'_id': key}, value, upsert=True)

def _createRowUpdateDict(row):
  date = row["date"]
  indexDate = date - timedelta(seconds=date.second)

  updatePath = "data." + row["country"] + "." + row["lob"] + "." + row["type"] + "."
  try:
    dataSize = int(row["dataSize"])
  except ValueError:
    print("ValueError: " + row["dataSize"])
    print(row)
    dataSize = 0
  update = {"$inc":
              {updatePath + row["flowName"]: dataSize,
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
