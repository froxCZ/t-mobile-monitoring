import unittest

import util
from mediation import MediationConfig
from mediation.flow_analyzer import FlowAnalyzer


class TestStringMethods(unittest.TestCase):
  def setUp(self):
    self.gsm = MediationConfig.getLobWithCountry("CZ", "GSM")

  def test_getLatestClosedIntervalTime(self):
    flow = self.gsm["flows"]["MSSCEB1B"]
    flow["options"]["granularity"] = 30
    lobAnalyzer = FlowAnalyzer(flow)
    testCases = [
      ("02.02.2017 15:35:03", "02.02.2017 15:00:00"),
      ("02.02.2017 18:03:00", "02.02.2017 17:30:00"),
      ("02.02.2017 01:00:00", "02.02.2017 00:30:00"),
      ("02.02.2017 00:15:03", "01.02.2017 23:30:00"),
      ("02.02.2017 00:00:00", "01.02.2017 23:30:00"),
      ("01.02.2017 23:59:59", "01.02.2017 23:00:00")
    ]
    for testCase in testCases:
      latestClosedIntervalTime = lobAnalyzer._getLatestCompleteTicTime(util.stringToTime(testCase[0]))
      self.assertEqual(latestClosedIntervalTime, util.stringToTime(testCase[1]))

  def test_getLatestClosedIntervalTimeOnDST(self):
    testCases = [
      ("26.03.2017 03:00:00", "26.03.2017 01:00:00", 60),
      ("29.10.2017 04:00:03", "29.10.2017 02:00:00", 120),
      ("29.10.2017 03:00:03", "29.10.2017 00:00:00", 120),
      ("26.03.2017 03:00:00", "26.03.2017 00:00:00", 120),
      ("27.03.2017 05:00:03", "26.03.2017 00:00:00", 1440),
      ("26.03.2017 05:00:03", "26.03.2017 00:00:00", 240),
      ("26.03.2017 05:00:03", "26.03.2017 03:00:00", 120),
      ("26.03.2017 03:00:03", "26.03.2017 02:55:00", 5)
    ]
    flow = self.gsm["flows"]["MSSCEB1B"]
    for testCase in testCases:
      flow["options"]["granularity"] = testCase[2]
      lobAnalyzer = FlowAnalyzer(flow)
      latestClosedIntervalTime = lobAnalyzer._getLatestCompleteTicTime(util.stringToTime(testCase[0]))
      expected = util.stringToTime(testCase[1])
      print(latestClosedIntervalTime == expected)
      self.assertEqual(latestClosedIntervalTime, expected)


if __name__ == '__main__':
  unittest.main()
