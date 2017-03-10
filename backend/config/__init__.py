import datetime

import pytz

from mongo import mongo
from .config import getLobConfig
from .config import getLobConfigByName
from .config import getLobsConfig

configColl = mongo.config()
TIMEZONE = pytz.timezone('CET')

_BASE_DATE_DIFF = datetime.timedelta(days=60)


def getCurrentTime():
  # return datetime.datetime.now().replace(tzinfo=TIMEZONE)
  return datetime.datetime.now().replace(tzinfo=TIMEZONE) - _BASE_DATE_DIFF


class Lob:
  def __init__(self, country, name, granularity=None, smooth=True):
    self.country = country;
    self.name = name
    self.granularity = granularity
    self.smooth = smooth


CZ_LOBS = {"SIS": Lob("CZ", "SIS", 180),
           "DWA": Lob("CZ", "DWA", 10),
           "MWB": Lob("CZ", "MWB", 60),
           "DAR": Lob("CZ", "DAR", 15),
           "SMS": Lob("CZ", "SMS", 60),
           "PCF": Lob("CZ", "PCF", 15),
           "PPC": Lob("CZ", "PPC", 15),
           "TCF": Lob("CZ", "TCF", 30),
           "GSM": Lob("CZ", "GSM", 15),
           "TPP": Lob("CZ", "TPP", 60),
           "XTC": Lob("CZ", "XTC", 15),
           "PST": Lob("CZ", "PST", 60),
           "WHS": Lob("CZ", "WHS", 10),
           "TAP": Lob("CZ", "TAP", 120),
           "SBC": Lob("CZ", "SBC", 90),
           "SCF": Lob("CZ", "SCF", 180),
           "LAS": Lob("CZ", "LAS", 15),
           "MMS": Lob("CZ", "MMS", 15),
           "ATS": Lob("CZ", "ATS", 15),
           "RRA": Lob("CZ", "RRA", 60),
           "VMS": Lob("CZ", "VMS", 60),
           "MTS": Lob("CZ", "MTS", 15),
           "OTA": Lob("CZ", "OTA", 30),
           "BVS": Lob("CZ", "BVS", 15),
           "VOP": Lob("CZ", "VOP", 20),
           "WEL": Lob("CZ", "WEL", 60),
           "CIR": Lob("CZ", "CIR", 60),
           "SMG": Lob("CZ", "SMG", 60),
           "LTP": Lob("CZ", "LTP", 1440),
           "M2M": Lob("CZ", "M2M", 1440),
           "EWG": Lob("CZ", "EWG", 180),
           "TIT": Lob("CZ", "TIT", 120),
           "RES": Lob("CZ", "RES", 1440),
           "KPI": Lob("CZ", "KPI", 1440),
           "EPC": Lob("CZ", "EPC", 120),
           "MNT": Lob("CZ", "MNT", 10),
           "TOC": Lob("CZ", "TOC", 1440),
           "EWH": Lob("CZ", "EWH", 60),
           "ACI": Lob("CZ", "ACI", 10),
           "ICG": Lob("CZ", "ICG", 60)}
LOBS = {"CZ": CZ_LOBS}


def getLobConfigByName(fullName):
  res = configColl.find_one({"_id": "lobs"}, {"lobs." + fullName: 1})
  tmp = fullName.split(".")
  country = tmp[0]
  lob = tmp[1]
  granularity = res["lobs"][country][lob]["granularity"]
  return Lob(country, lob, granularity)


def updateLob(lobName, lobUpdate):
  return configColl.update_one({"_id": "lobs"}, lobUpdate)
