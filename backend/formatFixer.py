import csv
import os

from mediation.data_receiver import DataReceiverUtil


class InputFormatFixer:
  def __init__(self, dirPath):
    super().__init__()
    self.dirPath = dirPath

  def fixDir(self):
    for filePath in os.listdir(self.dirPath):
      fullPath = os.path.join(self.dirPath, filePath)
      if os.path.isfile(fullPath):
        self.fixFile(fullPath)

  def fixFile(self, filePath):
    print(filePath)
    csvReader = csv.reader(open(filePath, "r"), delimiter=';', quotechar='"')
    inputRow = None
    for row in csvReader:
      inputRow = self.createInputRowV0(row)
      break
    date = DataReceiverUtil.stringToDate(inputRow["date"])
    newFileName = inputRow["country"] + "_Spark_Statistics_" + date.strftime("%y%m%d") + ".csv"
    csvWriter = csv.writer(open(os.path.join(self.dirPath, "formatted", newFileName), "w"),
                           delimiter=';', quotechar='"', quoting=csv.QUOTE_NONE)
    for row in csvReader:
      inputRow = self.createInputRowV0(row)
      try:
        csvWriter.writerow([0, inputRow["lob"], inputRow["flowName"], inputRow["dataSize"], inputRow["date"]])
      except Exception as e:
        print(e)

  def createInputRowV0(self, row):
    inputRow = {}
    inputRow["country"] = row[1]
    inputRow["lob"] = row[2]
    inputRow["type"] = "inputs"
    inputRow["flowName"] = row[3]
    inputRow["dataSize"] = row[5]
    inputRow["date"] = row[6]
    return inputRow

class ForwardFormatFixer:
  def __init__(self, dirPath,country):
    super().__init__()
    self.dirPath = dirPath
    self.country = country

  def fixDir(self):
    for filePath in os.listdir(self.dirPath):
      fullPath = os.path.join(self.dirPath, filePath)
      if os.path.isfile(fullPath):
        self.fixFile(fullPath)

  def fixFile(self, filePath):
    print(filePath)
    csvReader = csv.reader(open(filePath, "r"), delimiter='|', quotechar='"')
    inputRow = None
    for row in csvReader:
      inputRow = self.createForwardRowV0(row)
      break
    date = DataReceiverUtil.stringToDate(inputRow["date"])
    newFileName = self.country + "_Spark_Statistics_" + date.strftime("%y%m%d") + ".csv"
    csvWriter = csv.writer(open(os.path.join(self.dirPath, "formatted", newFileName), "w"),
                           delimiter=';', quotechar='"', quoting=csv.QUOTE_NONE)
    for row in csvReader:
      inputRow = self.createForwardRowV0(row)
      try:
        csvWriter.writerow([0, inputRow["lob"], inputRow["neid"],inputRow["target"], inputRow["dataSize"], inputRow["date"]])
      except Exception as e:
        print(e)

  def createForwardRowV0(self, row):
    forward = {}
    forward["type"] = "forwards"
    forward["lob"] = row[0].strip()
    forward["neid"] = row[1].strip()
    forward["target"] = row[2].strip()
    forward["flowName"] = forward["neid"] + ":" + forward["target"]
    forward["dataSize"] = int(row[3].strip())
    forward["date"] = row[5]
    return forward


#ForwardFormatFixer("/home/frox/tmobile/data_mar12/preparation/output/CZ/csv","CZ").fixDir()
ForwardFormatFixer("/home/frox/tmobile/data_mar12/preparation/output/NL/csv","NL").fixDir()
ForwardFormatFixer("/home/frox/tmobile/data_mar12/preparation/output/AT/csv","AT").fixDir()
ForwardFormatFixer("/home/frox/tmobile/data_mar12/preparation/output/DE/csv","DE").fixDir()
