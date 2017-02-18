import datetime

import dateutil.parser


def jsStringToDate(string):
  return dateutil.parser.parse(string) \
         - datetime.timedelta(hours=10)  # hack while dates in mongo are at 00:00Z instead of 00:00CET
