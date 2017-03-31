import csv

import pytz

from mediation.data_receiver import DataReceiverConfig
from mediation.data_receiver import DataReceiverUtil

LATEST_DATE = DataReceiverUtil.stringToDate("20.02.16 00:00:00")


def isValidFlow(flow):
  return flow["date"] > LATEST_DATE and flow["country"] + "_" + flow["lob"] not in DataReceiverConfig.IGNORE_LOBS


def createInputRow(row):
  inputRow = {}
  inputRow["country"] = row[1]
  inputRow["lob"] = row[2]
  inputRow["type"] = "inputs"
  inputRow["flowName"] = row[3]
  inputRow["dataSize"] = row[5]
  inputRow["date"] = DataReceiverUtil.stringToDate(row[6]).replace(tzinfo=pytz.timezone('CET'))
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
