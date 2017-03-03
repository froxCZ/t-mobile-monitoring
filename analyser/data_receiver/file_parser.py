import csv

import pytz

import data_receiver.util as util
from config import config
from data_receiver import data_insertor


class FileParser:
  def __init__(self):
    pass

  def parseInputs(self, inputFile):
    inputsList = []
    dataInsertor = data_insertor.DataInsertor()
    with open(inputFile, 'r') as csvfile:
      spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
      for row in spamreader:
        try:
          if row[1] in config.LOBS and row[2] in config.LOBS[row[1]]:
            inputsList.append(self.createLobRow(row))
        except Exception as e:
          print("exception:")
          print(row)
          print(e)
          print("---")
        if len(inputsList) >= 100000:
          dataInsertor.insertInputs(inputsList)
          inputsList = []
    dataInsertor.insertInputs(inputsList)

  def createLobRow(self, row):
    inputRow = {}
    inputRow["country"] = row[1]
    inputRow["lob"] = row[1] + "_" + row[2]
    inputRow["neid"] = row[3]
    inputRow["dataSize"] = row[5]
    inputRow["date"] = util.stringToDate(row[6]).replace(tzinfo=pytz.timezone('CET'))
    return inputRow
