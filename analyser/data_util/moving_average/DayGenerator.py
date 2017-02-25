import datetime

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


def getPastSimilarDays(lobName, date, days=10):
  if (_isWorkDay(date)):
    return _getPastWorkDays(lobName, date, days)
  if (_isWeekendDay(date)):
    return _getPastWeekends(lobName, date, days)


def _getPastWorkDays(lobName, date, days=10):
  resultDays = []
  i = 1
  while len(resultDays) <= days:
    dayToTest = date - datetime.timedelta(days=i)
    if _isWorkDay(dayToTest):
      resultDays.append(dayToTest)
    i += 1
  return resultDays


def _getPastWeekends(lobName, date, days=10):
  resultDays = []
  i = 1
  while len(resultDays) <= days:
    dayToTest = date - datetime.timedelta(days=i)
    if _isWeekendDay(dayToTest):
      resultDays.append(dayToTest)
    i += 1
  return resultDays


def _isWorkDay(date):
  if (date.weekday() >= 5):
    return False
  return not _isHoliday(date)


def _isWeekendDay(date):
  return date.weekday() >= 5


def _isHoliday(date):
  for i in HOLIDAYS:
    if date.day == i[0] and date.month == i[1]:
      return True
  return False