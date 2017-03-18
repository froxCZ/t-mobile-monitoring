import datetime
import os

from mediation.data_receiver.file_parser import FileParser

dirPath = os.path.dirname(os.path.realpath(__file__))
print(dirPath)
print(datetime.datetime.now())

fileParser = FileParser()
# fileParser.parseInputs(dirPath + "/input/all_inputs.csv")
# print("finished inserting inputs")
# print(datetime.datetime.now())
fileParser.parseForwards("NL", "../../input/nl_forwards.csv")
print("finished inserting forwards")
# print(datetime.datetime.now())
