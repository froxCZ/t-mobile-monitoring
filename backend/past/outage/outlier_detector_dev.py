from mediation.api import util
from past.outage import OutlierDetector

outlierDetector = OutlierDetector("CZ.GSM", util.jsStringToDate("2016-10-11T12:30:00.000Z"))
status = outlierDetector.getOutageStatus()
print(status)
