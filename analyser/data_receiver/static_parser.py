import csv

import pytz

import data_receiver.util as util
from config import config
from data_receiver import data_insertor


class StaticParser:
  def __init__(self, inputFile):
    self.inputFile = inputFile

  def run(self):
    lobRows = []
    with open(self.inputFile, 'r') as csvfile:
      spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
      for row in spamreader:
        try:
          if row[1] in config.LOBS and row[2] in config.LOBS[row[1]]:
            lobRows.append(self.createLobRow(row))
        except Exception as e:
          print("exception:")
          print(row)
          print(e)
          print("---")
        if len(lobRows) >= 50000:
          data_insertor.insertData(lobRows)
          lobRows = []
    data_insertor.insertData(lobRows)

  def createLobRow(self, row):
    lobRow = {}
    lobRow["country"] = row[1]
    lobRow["lob"] = row[2]
    lobRow["sourceName"] = row[3]
    lobRow["dataSize"] = row[5]
    lobRow["date"] = util.stringToDate(row[6]).replace(tzinfo=pytz.timezone('CET'))
    return lobRow


class LobRow:
  def __init__(self):
    pass

#
# def splitByLob(input,outputDir):
#     fileWriters = {}
#     import shutil
#     if os.path.exists(outputDir):
#         shutil.rmtree(outputDir)
#     os.makedirs(outputDir)
#     with open(input, 'r') as csvfile:
#         spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
#         for row in spamreader:
#             lobName = row[1]+"_"+row[2]#country_lobname
#             if lobName == "GT2":
#                 continue
#             if lobName in fileWriters:
#                 fileWriter = fileWriters[lobName]
#             else:
#                 fileWriter = open(outputDir+"/"+lobName+".csv",'w')
#                 fileWriters[lobName] = fileWriter
#                 print(lobName)
#             fileWriter.write(";".join(row)+"\n")
#
#
#
# class LobRow():
#     def __init__(self,row):
#         self.stamp = row[0]
#         self.name = row[2]
#         self.country = row[1]
#         self.sourceName = row[3]
#         self.dataSize = int(row[-2])
#         self.date = util.stringToDate(row[-1])
#
#
# def granularityDetector(input):
#     with open(input, 'r') as csvfile:
#         spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
#         rows = []
#         for row in spamreader:
#             lobRow = LobRow(row)
#             rows.append(lobRow)
#         rows.sort(key=lambda x:x.date)
#         sources = {}
#         for row in rows:
#             print(row.stamp+" "+row.sourceName + str(row.date))
#             if row.sourceName in sources:
#                 diff = row.date - sources[row.sourceName].date
#                 if diff.total_seconds() > 60:
#                     return int(diff.total_seconds()/60)
#                 else:
#                     sources[row.sourceName] = row
#             else:
#                 sources[row.sourceName] = row

#
# for lob in config.LOB_NAMES:
#     granularity = granularityDetector(config.DATA_DIR+"/byLob/"+lob+".csv")
#     if granularity<=10:
#         granularity = 10
#     elif granularity<=15:
#         granularity = 15
#     elif granularity<=20:
#         granularity = 20
#     elif granularity<=30:
#         granularity=30
#     elif granularity<=60:
#         granularity = 60
#     elif granularity<=120:
#         granularity = 120
#     elif granularity<=180:
#         granularity = 180
#     elif granularity<=60*24:
#         granularity = 60*24
#     else:
#         raise Exception("no granularity for "+str(granularity)+" lob "+lob)
#     print("Lob("+lob+","+str(granularity)+")")
