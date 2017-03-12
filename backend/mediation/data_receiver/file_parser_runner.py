import datetime

from mediation.data_receiver.file_parser import FileParser

print(datetime.datetime.now())

fileParser = FileParser()
fileParser.parseInputs("../../input/cz_inputs.csv")
print("finished inserting inputs")
print(datetime.datetime.now())
fileParser.parseForwards("CZ", "../../input/cz_forwards.csv")
print("finished inserting forwards")
print(datetime.datetime.now())
