from support_development_packages.outage import OutlierDetector

from mediation.api import util

outlierDetector = OutlierDetector("CZ.GSM", util.jsStringToDate("2016-10-11T12:30:00.000Z"))
status = outlierDetector.getOutageStatus()
print(status)
