import datetime


def jsStringToDate(string):
  return datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%S.%fZ')