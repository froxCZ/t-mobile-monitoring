import logging
import os
from datetime import timedelta

from mediation.data_receiver.DataParser import DataParser
from mongo import mongo


class DataInsertor():
  def __init__(self, version=-1):
    super().__init__()
    self.version = version

  def insertDir(self, dirPath, type, country):
    for filePath in os.listdir(dirPath):
      self.insertFile(os.path.join(dirPath, filePath), type, country)

  def insertFile(self, filePath, type, country):
    dataParser = DataParser(open(filePath, "r"), type, country, self.version)
    logging.info("Inserting file " + filePath)
    for dataList in dataParser:
      self._insertRows(dataList)

  def run(self, stream):
    self.dataParser = DataParser(stream)
    for dataList in self.dataParser:
      self._insertRows(dataList)

  def _insertRows(self, rowList):
    coll = mongo.lobs()
    updates = _sumUpdates(list(map(_createRowUpdateDict, rowList)))
    logging.info("Inserted " + str(len(rowList)) + " rows")
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


if __name__ == "__main__":
  insertor = DataInsertor()
  insertor.run(open("/home/frox/tmobile/data_mar12/preparation/input/AT_Spark_Statistics_010117.csv", 'r'))
