import sys

def load():
  paths = ['/home/frox/school/thesis/nodejs/bigmon/backend']
  for p in paths:
    sys.path.insert(0, p)
load()