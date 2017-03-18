import csv

import pytz

import mediation.data_receiver.config as config
import mediation.data_receiver.util as util
from config import AppConfig
from .data_insertor import DataInsertor

LATEST_DATE = util.stringToDate("20.02.16 00:00:00").replace(tzinfo=AppConfig.getTimezone())


def isValidFlow(flow):
  return flow["date"] > LATEST_DATE and flow["country"] in config.COUNTRIES and flow["lob"] not in config.IGNORE_LOBS


class FileParser:
  def __init__(self):
    self.batchSize = 100000

  def parseInputs(self, inputFile):
    inputsList = []
    dataInsertor = DataInsertor()
    with open(inputFile, 'r') as csvfile:
      spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
      for row in spamreader:
        try:
          input = self.createInputRow(row)
          if isValidFlow(input):
            inputsList.append(input)
        except Exception as e:
          print("exception:")
          print(row)
          print(e)
          print("---")
        if len(inputsList) >= self.batchSize:
          dataInsertor.insertRows(inputsList)
          inputsList = []
    dataInsertor.insertRows(inputsList)

  def createInputRow(self, row):
    inputRow = {}
    inputRow["country"] = row[1]
    inputRow["lob"] = row[2]
    inputRow["type"] = "inputs"
    inputRow["flowName"] = row[3]
    inputRow["dataSize"] = row[5]
    inputRow["date"] = util.stringToDate(row[6]).replace(tzinfo=pytz.timezone('CET'))
    return inputRow

  def parseForwards(self, country, file):
    forwards = []
    dataInsertor = DataInsertor()
    with open(file, 'r') as csvfile:
      spamreader = csv.reader(csvfile, delimiter='|', quotechar='"')
      for row in spamreader:
        try:
          forward = self.createForwardRow(country, row)
          if isValidFlow(forward):
            forwards.append(forward)
        except Exception as e:
          print("exception:")
          print(row)
          print(e)
          print("---")
        if len(forwards) >= self.batchSize:
          dataInsertor.insertRows(forwards)
          forwards = []
    dataInsertor.insertRows(forwards)

  def createForwardRow(self, country, row):
    forward = {}
    forward["country"] = country
    forward["type"] = "forwards"
    forward["lob"] = row[0].strip()
    forward["neid"] = row[1].strip()
    forward["target"] = row[2].strip()
    forward["flowName"] = forward["neid"] + ":" + forward["target"]
    forward["dataSize"] = int(row[3].strip())
    forward["date"] = util.stringToDate(row[5]).replace(tzinfo=pytz.timezone('CET'))
    return forward
