import datetime

import util
from config import config

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


class SimilarPastDaysFinder():
  def __init__(self, lobNames, inputs, forwards):
    self.lobNames = lobNames
    self.inputs = inputs
    self.forwards = forwards
    if len(inputs) > 0:
      self.options = config.getOptions(lobNames[0], inputs[0], None)
    elif len(forwards) > 0:
      self.options = config.getOptions(lobNames[0], None, forwards[0])
    else:
      raise Exception("no inputs or forwards specified")
    self.independentdays = self.options.get("independentdays", [])

  def findSimilarPastDays(self, date):
    self.date = date
    if (_isWorkDay(self.date)):
      return self._getPastWorkDays()
    if (_isWeekendDay(self.date)):
      return self._getPastWeekends()
    if (_isHoliday(self.date)):
      return self._getPastHolidays()

  def _getPastHolidays(self):
    resultDays = []
    i = 1
    dayToTest = self.date
    while len(resultDays) < 4 and dayToTest > INITIAL_DATE:
      dayToTest -= datetime.timedelta(days=1)
      if _isHoliday(dayToTest) and _isUsualDay(dayToTest):
        resultDays.append(dayToTest)
      i += 1

    return resultDays

  def _getPastWorkDays(self, days=5):
    resultDays = []
    i = 1
    date = self.date
    while len(resultDays) < days:
      dayToTest = date - datetime.timedelta(days=i)
      if _isWorkDay(dayToTest) and _isUsualDay(dayToTest) and self._satifiesIndependentDays(dayToTest):
        resultDays.append(dayToTest)
      i += 1
    return resultDays

  def _satifiesIndependentDays(self, dayToTest):
    if self.date.weekday() in self.independentdays:
      return self.date.weekday() == dayToTest.weekday()
    return True

  def _isSameWorkDay(self, dateToTest):
    date = self.date
    if date.weekday() == 0 or date.weekday() == 4:
      return date.weekday() == dateToTest.weekday()
    else:
      return True

  def _getPastWeekends(self, days=4):
    resultDays = []
    i = 1
    date = self.date
    while len(resultDays) < days:
      dayToTest = date - datetime.timedelta(days=i)
      if _isWeekendDay(dayToTest) and _isUsualDay(dayToTest) and self._satifiesIndependentDays(dayToTest):
        resultDays.append(dayToTest)
      i += 1
    return resultDays

  def _getSameWeekendDay(self, days=10):
    resultDays = []
    i = 1
    while len(resultDays) < days:
      dayToTest = self.date - datetime.timedelta(days=i)
      if self.date.weekday() == dayToTest.weekday() and _isUsualDay(dayToTest):
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
