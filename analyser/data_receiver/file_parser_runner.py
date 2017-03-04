from data_receiver.file_parser import FileParser

fileParser = FileParser()
# fileParser.parseInputs("../input/all_cz.csv");
fileParser.parseForwards("CZ","../input/cz_forwards.csv")
