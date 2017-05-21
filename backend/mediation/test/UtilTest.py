import datetime
import unittest

import pytz

from common import util

PRAGUE_TIMEZONE = pytz.timezone("Europe/Prague")


class UtilTest(unittest.TestCase):
  def setUp(self):
    pass

  def test_stringToDate(self):
    self.assertEqual(util.stringToDate("01.02.2017"), UtilTest.localizeTime(datetime.datetime(2017, 2, 1)))
    self.assertEqual(util.stringToDate("01.03.2017"), UtilTest.localizeTime(datetime.datetime(2017, 3, 1)))
    self.assertEqual(util.stringToDate("01.05.2017"), UtilTest.localizeTime(datetime.datetime(2017, 5, 1)))
    self.assertEqual(util.stringToDate("01.06.2017"), UtilTest.localizeTime(datetime.datetime(2017, 6, 1)))

  def test_stringToTime(self):
    self.assertEqual(util.stringToTime("01.02.2017 02:00:00"),
                     UtilTest.localizeTime(datetime.datetime(2017, 2, 1, 2, 00, 00)))
    self.assertEqual(util.stringToTime("26.03.2017 02:00:00"),
                     UtilTest.localizeTime(datetime.datetime(2017, 3, 26, 2, 00, 00)))
    self.assertEqual(util.stringToTime("26.03.2017 03:00:00"),
                     UtilTest.localizeTime(datetime.datetime(2017, 3, 26, 3, 00, 00)))

  def test_dateToTimeString(self):
    self.assertEqual(util.dateToTimeString(util.stringToTime("01.02.2017 02:00:00")),
                     "2017-02-01T02:00:00+01:00")
    self.assertEqual(util.dateToTimeString(util.stringToTime("26.03.2017 02:00:00")),
                     "2017-03-26T02:00:00+01:00")
    self.assertEqual(util.dateToTimeString(util.stringToTime("26.03.2017 03:00:00")),
                     "2017-03-26T03:00:00+02:00")

  def test_dateDataListToList(self):
    metricName = "metric"
    dateDataList = [{metricName: 30}, {metricName: 40}, {metricName: 50}]
    resList = util.dateDataListToList(dateDataList, metricName)
    self.assertEqual(resList[0], 30)
    self.assertEqual(resList[1], 40)
    self.assertEqual(resList[2], 50)

  def test_dateToDayMinutes(self):
    self.assertEqual(util.dateToDayMinutes(util.stringToTime("01.02.2017 02:00:00")), 120)
    self.assertEqual(util.dateToDayMinutes(util.stringToTime("01.02.2017 03:00:00")), 180)
    self.assertEqual(util.dateToDayMinutes(util.stringToTime("26.03.2017 04:00:00")), 240)

  def test_resetDateTimeMidnight(self):
    self.assertEqual(util.resetDateTimeMidnight(util.stringToTime("01.02.2017 02:00:00")),
                     util.stringToTime("01.02.2017 00:00:00"))
    self.assertEqual(util.resetDateTimeMidnight(util.stringToTime("02.02.2017 03:00:00")),
                     util.stringToTime("02.02.2017 00:00:00"))
    self.assertEqual(util.resetDateTimeMidnight(util.stringToTime("26.03.2017 04:00:00")),
                     util.stringToTime("26.03.2017 00:00:00"))

  def test_minuteDictToDateDict(self):
    baseDate = util.stringToTime("01.02.2017 00:00:00")
    tickDelta = datetime.timedelta(minutes=30)
    dayMinutes = {30: 10, 60: 20, 90: 30}
    metric = "metric"
    dateDict = util.minuteDictToDateDict(baseDate, dayMinutes, metric)
    self.assertEqual(dateDict[baseDate + tickDelta][metric], 10)
    self.assertEqual(dateDict[baseDate + tickDelta * 2][metric], 20)
    self.assertEqual(dateDict[baseDate + tickDelta * 3][metric], 30)

  def test_merge2DateLists(self):
    val1 = "val1"
    val2 = "val2"
    list1 = [{"_id": 1, val1: 1}, {"_id": 2, val1: 2}, {"_id": 4, val1: 4}]
    list2 = [{"_id": 1, val2: 10}, {"_id": 5, val2: 50}, {"_id": 3, val2: 30}]
    mergedList = util.merge2DateLists(list1, [val1], list2, [val2])
    self.assertEqual(mergedList[0][val1], 1)
    self.assertEqual(mergedList[0][val2], 10)
    self.assertEqual(mergedList[1][val1], 2)
    self.assertEqual(mergedList[1][val2], 0)
    self.assertEqual(mergedList[2][val1], 0)
    self.assertEqual(mergedList[2][val2], 30)
    self.assertEqual(mergedList[3][val1], 4)
    self.assertEqual(mergedList[3][val2], 0)
    self.assertEqual(mergedList[4][val1], 0)
    self.assertEqual(mergedList[4][val2], 50)
    pass

  def test_dictToSortedList(self):
    dict = {1: 0, 3: 5, -2: -2}
    sortedList = util.dictToSortedList(dict)
    self.assertEqual(sortedList[0], -2)
    self.assertEqual(sortedList[1], 0)
    self.assertEqual(sortedList[2], 5)

  def test_getNextTic(self):
    testCases = [
      ("26.03.2017 02:00:00", "26.03.2017 04:00:00", 60),
      ("26.03.2017 03:00:00", "26.03.2017 04:00:00", 60),
      ("26.03.2017 01:00:00", "26.03.2017 03:00:00", 180),
      ("26.03.2017 01:55:00", "26.03.2017 03:00:00", 15),
      ("26.03.2017 08:10:00", "26.03.2017 09:00:00", 60),
    ]
    for testCase in testCases:
      time = util.stringToTime(testCase[0])
      expected = util.stringToTime(testCase[1])
      granularity = testCase[2]
      self.assertEqual(util.getNextTic(time, granularity), expected, "time: " + str(time))

  def test_getNextDay(self):
    testCases = [
      ("23.03.2017 00:00:00", "24.03.2017 00:00:00"),
      ("25.03.2017 00:00:00", "26.03.2017 00:00:00"),
      ("26.03.2017 00:00:00", "27.03.2017 00:00:00"),
    ]
    for testCase in testCases:
      day = util.stringToTime(testCase[0])
      nextDay = util.stringToTime(testCase[1])
      self.assertEqual(util.getNextDay(day), nextDay)

  @staticmethod
  def localizeTime(datetime):
    return PRAGUE_TIMEZONE.localize(datetime)


if __name__ == '__main__':
  unittest.main()
