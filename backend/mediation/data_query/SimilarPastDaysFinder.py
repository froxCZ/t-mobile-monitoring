import datetime

import util
from mediation import MediationConfig

INITIAL_DATE = util.stringToDate("01.08.2016")

IGNORE_DAYS = [(24, 12), (31, 12), (1, 1)] #days with always unusual traffic. Do not use for expectations


class SimilarPastDaysFinder():
  """
  Finds similar days for the given day and flow
  """
  def __init__(self, flow):
    self.options = flow["options"]
    self.independentDays = self.options.get("independentDays", [])
    self.country = MediationConfig.getCountryByName(flow["country"])
    self.HOLIDAYS = []
    for holiday in self.country["holidays"]:
      day, month = holiday.split(".")
      self.HOLIDAYS.append((int(day), int(month)))
    pass

  def findSimilarPastDays(self, date):
    self.date = date
    if (self._isWorkDay(self.date)):
      return self._getPastWorkDays()
    if (self._isWeekendDay(self.date)):
      return self._getPastWeekends()
    if (self._isHoliday(self.date)):
      return self._getPastWeekends()

  def _getPastHolidays(self):
    resultDays = []
    i = 1
    dayToTest = self.date
    while len(resultDays) < 4 and dayToTest > INITIAL_DATE:
      dayToTest -= datetime.timedelta(days=1)
      if self._isHoliday(dayToTest) and self._isUsualDay(dayToTest):
        resultDays.append(dayToTest)
      i += 1

    return resultDays

  def _getPastWorkDays(self, days=5):
    resultDays = []
    i = 1
    date = self.date
    while len(resultDays) < days:
      dayToTest = date - datetime.timedelta(days=i)
      if self._isWorkDay(dayToTest) and self._isUsualDay(dayToTest) and self._satifiesIndependentDays(dayToTest):
        resultDays.append(dayToTest)
      i += 1
    return resultDays

  def _satifiesIndependentDays(self, dayToTest):
    if self.date.weekday() in self.independentDays:
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
      if self._isWeekendDay(dayToTest) and self._isUsualDay(dayToTest) and self._satifiesIndependentDays(dayToTest):
        resultDays.append(dayToTest)
      i += 1
    return resultDays

  def _getSameWeekendDay(self, days=10):
    resultDays = []
    i = 1
    while len(resultDays) < days:
      dayToTest = self.date - datetime.timedelta(days=i)
      if self.date.weekday() == dayToTest.weekday() and self._isUsualDay(dayToTest):
        resultDays.append(dayToTest)
      i += 1
    return resultDays

  def _isWorkDay(self, date):
    if (date.weekday() >= 5):
      return False
    return not self._isHoliday(date)

  def _isWeekendDay(self, date):
    return date.weekday() >= 5

  def _isUsualDay(self, date):
    for i in IGNORE_DAYS:
      if date.day == i[0] and date.month == i[1]:
        return False
    return True

  def _isHoliday(self, date):
    for i in self.HOLIDAYS:
      if date.day == i[0] and date.month == i[1]:
        return True
    return False
