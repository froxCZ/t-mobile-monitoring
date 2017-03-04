import csv

import pytz

import data_receiver.util as util
from config import config
from data_receiver import data_insertor


class FileParser:
  def __init__(self):
    self.batchSize = 100000

  def parseInputs(self, inputFile):
    inputsList = []
    dataInsertor = data_insertor.DataInsertor()
    with open(inputFile, 'r') as csvfile:
      spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
      for row in spamreader:
        try:
          if row[1] in config.LOBS and row[2] in config.LOBS[row[1]]:
            inputsList.append(self.createInputRow(row))
        except Exception as e:
          print("exception:")
          print(row)
          print(e)
          print("---")
        if len(inputsList) >= self.batchSize:
          dataInsertor.insertInputs(inputsList)
          inputsList = []
    dataInsertor.insertInputs(inputsList)

  def createInputRow(self, row):
    inputRow = {}
    inputRow["country"] = row[1]
    inputRow["lob"] = row[1] + "_" + row[2]
    inputRow["neid"] = row[3]
    inputRow["dataSize"] = row[5]
    inputRow["date"] = util.stringToDate(row[6]).replace(tzinfo=pytz.timezone('CET'))
    return inputRow

  def parseForwards(self, country, file):
    forwards = []
    dataInsertor = data_insertor.DataInsertor()
    with open(file, 'r') as csvfile:
      spamreader = csv.reader(csvfile, delimiter='|', quotechar='"')
      for row in spamreader:
        try:
          if country in config.LOBS and row[0].strip() in config.LOBS[country]:
            forwards.append(self.createForwardRow(country, row))
        except Exception as e:
          print("exception:")
          print(row)
          print(e)
          print("---")
        if len(forwards) >= self.batchSize:
          dataInsertor.insertForwards(forwards)
          forwards = []
    dataInsertor.insertForwards(forwards)

  def createForwardRow(self, country, row):
    forward = {}
    forward["lob"] = country + "_" + row[0].strip()
    forward["neid"] = row[1].strip()
    forward["target"] = row[2].strip()
    forward["forward"] = forward["neid"] + ":" + forward["target"]
    forward["dataSize"] = int(row[3].strip())
    forward["date"] = util.stringToDate(row[5]).replace(tzinfo=pytz.timezone('CET'))
    return forward
