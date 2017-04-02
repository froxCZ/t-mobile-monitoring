import csv

import pytz

from mediation.data_receiver import DataReceiverConfig
from mediation.data_receiver import DataReceiverUtil

LATEST_DATE = DataReceiverUtil.stringToDate("20.02.16 00:00:00")
utc = pytz.timezone('UTC')


def isValidDate(d):
  return d > LATEST_DATE


def isValidFlow(flow):
  return flow["country"] + "_" + flow["lob"] not in DataReceiverConfig.IGNORE_LOBS


LATEST_VERSION = 1


class DataParser:
  def __init__(self, stream, type, country, version):
    self.batchSize = 10000
    self.reader = csv.reader(stream, delimiter=';', quotechar='"')
    self.type = type
    self.country = country
    self.version = version
    if version == -1:
      self.version = LATEST_VERSION
    self.createInputRow = [self.createInputRowV0, self.createInputRowV1][self.version]
    self.createForwardRow = [None, self.createForwardRowV1][self.version]

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
        if not isValidDate(row["date"]):
          raise StopIteration
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

  def createInputRowV0(self, row):
    inputRow = {}
    inputRow["country"] = row[1]
    inputRow["lob"] = row[2]
    inputRow["type"] = "inputs"
    inputRow["flowName"] = row[3]
    inputRow["dataSize"] = int(row[5])
    inputRow["date"] = DataReceiverUtil.stringToDate(row[6]).astimezone(utc)
    return inputRow

  def createInputRowV1(self, row):
    inputRow = {}
    inputRow["country"] = self.country
    inputRow["lob"] = row[1]
    inputRow["type"] = "inputs"
    inputRow["flowName"] = row[2]
    inputRow["dataSize"] = row[3]
    inputRow["date"] = DataReceiverUtil.stringToDate(row[4]).astimezone(utc)
    return inputRow

  def createForwardRowV1(self, row):
    inputRow = {}
    inputRow["country"] = self.country
    inputRow["lob"] = row[1]
    inputRow["type"] = "forwards"
    inputRow["flowName"] = row[2] + ":" + row[3]
    inputRow["dataSize"] = row[4]
    inputRow["date"] = DataReceiverUtil.stringToDate(row[5]).astimezone(utc)
    return inputRow
