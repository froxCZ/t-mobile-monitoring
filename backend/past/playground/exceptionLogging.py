import logging

try:
  raise Exception("asxxxxd")
except Exception as e:
  logging.exception("xx")