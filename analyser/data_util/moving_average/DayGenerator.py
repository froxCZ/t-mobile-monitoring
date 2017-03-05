import datetime

import util

HOLIDAYS = [(1, 1),  # day, month
            (1, 1),
            (17, 4),
            (14, 4),
            (1, 5),
            (8, 5),
            (5, 7),
            (6, 7),
            (28, 9),
            (28, 10),
            (17, 11),
            (24, 12),
            (25, 12),
            (26, 12), ]

INITIAL_DATE = util.stringToDate("01.08.2016")

IGNORE_DAYS = [(24, 12), (31, 12), (1, 1)]


def _getPastHolidays(lobName, date, days):
  resultDays = []
  i = 1
  dayToTest = date
  while len(resultDays) <= days and dayToTest > INITIAL_DATE:
    dayToTest -= datetime.timedelta(days=1)
    if _isHoliday(dayToTest) and _isUsualDay(dayToTest):
      resultDays.append(dayToTest)
    i += 1

  return resultDays


def getPastSimilarDays(lobName, date, days=10):
  if (_isWorkDay(date)):
    return _getPastWorkDays(lobName, date, days)
  if (_isWeekendDay(date)):
    return _getPastWeekends(lobName, date, 4)
  if (_isHoliday(date)):
    return _getPastHolidays(lobName, date, 4)


def _getPastWorkDays(lobName, date, days=10):
  resultDays = []
  i = 1
  while len(resultDays) <= 4:
    dayToTest = date - datetime.timedelta(days=i)
    if _isWorkDay(dayToTest) and _isUsualDay(dayToTest):# and _isSameWorkDay(date, dayToTest):
      resultDays.append(dayToTest)
    i += 1
  return resultDays


def _isSameWorkDay(date, dateToTest):
  if date.weekday() == 0 or date.weekday() == 4:
    return date.weekday() == dateToTest.weekday()
  else:
    return True

def _getPastWeekends(lobName, date, days=10):
  resultDays = []
  i = 1
  while len(resultDays) <= days:
    dayToTest = date - datetime.timedelta(days=i)
    if _isWeekendDay(dayToTest) and _isUsualDay(dayToTest):
      resultDays.append(dayToTest)
    i += 1
  return resultDays


def _getSameWeekendDay(lobName, date, days=10):
  resultDays = []
  i = 1
  while len(resultDays) < days:
    dayToTest = date - datetime.timedelta(days=i)
    if date.weekday() == dayToTest.weekday() and _isUsualDay(dayToTest):
      resultDays.append(dayToTest)
    i += 1
  return resultDays


def _isWorkDay(date):
  if (date.weekday() >= 5):
    return False
  return not _isHoliday(date)


def _isWeekendDay(date):
  return date.weekday() >= 5


def _isUsualDay(date):
  for i in IGNORE_DAYS:
    if date.day == i[0] and date.month == i[1]:
      return False
  return True


def _isHoliday(date):
  for i in HOLIDAYS:
    if date.day == i[0] and date.month == i[1]:
      return True
  return False
