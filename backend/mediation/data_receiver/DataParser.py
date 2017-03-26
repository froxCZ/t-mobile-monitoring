import csv

import pytz

from config import AppConfig
from mediation.data_receiver import DataListInsertor
from mediation.data_receiver import config
from mediation.data_receiver import util

LATEST_DATE = util.stringToDate("20.02.16 00:00:00").replace(tzinfo=AppConfig.getTimezone())


def isValidFlow(flow):
  return flow["date"] > LATEST_DATE and flow["country"] + "_" + flow["lob"] not in config.IGNORE_LOBS


def createInputRow(row):
  inputRow = {}
  inputRow["country"] = row[1]
  inputRow["lob"] = row[2]
  inputRow["type"] = "inputs"
  inputRow["flowName"] = row[3]
  inputRow["dataSize"] = row[5]
  inputRow["date"] = util.stringToDate(row[6]).replace(tzinfo=pytz.timezone('CET'))
  return inputRow


class DataParser:
  def __init__(self, stream):
    self.batchSize = 10000
    self.reader = csv.reader(stream, delimiter=';', quotechar='"')

  def __iter__(self):
    return self

  def __next__(self):
    inputsList = []
    for row in self.reader:
      try:
        input = createInputRow(row)
        if isValidFlow(input):
          inputsList.append(input)
      except Exception as e:
        print("exception:")
        print(row)
        print(e)
        print("---")
      if len(inputsList) >= self.batchSize:
        return inputsList
    if len(inputsList) > 0:
      return inputsList
    raise StopIteration  # Done iterating.


if __name__ == "__main__":
  insertor = DataListInsertor()
  for i in DataParser(
    open("/home/frox/tmobile/data_mar12/preparation/input/AT_Spark_Statistics_010117.csv", 'r')):
    insertor.insertRows(i)
