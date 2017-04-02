import csv

import pytz

from mediation.data_receiver import DataReceiverConfig
from mediation.data_receiver import DataReceiverUtil

LATEST_DATE = DataReceiverUtil.stringToDate("20.02.16 00:00:00")
utc = pytz.timezone('UTC')

def isValidFlow(flow):
  return flow["date"] > LATEST_DATE and flow["country"] + "_" + flow["lob"] not in DataReceiverConfig.IGNORE_LOBS





class DataParser:
  def __init__(self, stream, type, country):
    self.batchSize = 10000
    self.reader = csv.reader(stream, delimiter=';', quotechar='"')
    self.type = type
    self.country = country

  def __iter__(self):
    return self

  def __next__(self):
    inputsList = []
    for row in self.reader:
      try:
        if self.type == "inputs":
          row = self.createInputRow(row)
        elif self.type == "forwards":
          row = self.createForwardRow(row)
        if isValidFlow(row):
          inputsList.append(row)
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

  def createInputRow(self,row):
    inputRow = {}
    inputRow["country"] = self.country
    inputRow["lob"] = row[1]
    inputRow["type"] = "inputs"
    inputRow["flowName"] = row[2]
    inputRow["dataSize"] = row[3]
    inputRow["date"] = DataReceiverUtil.stringToDate(row[4]).astimezone(utc)
    return inputRow

  def createForwardRow(self, row):
    pass
