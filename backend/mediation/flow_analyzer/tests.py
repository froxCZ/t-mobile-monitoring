import unittest

import config
import util
from mediation.flow_analyzer import FlowAnalyzer


class TestStringMethods(unittest.TestCase):
  def setUp(self):
    gsm = config.getLobConfig("CZ_GSM")
    self.lobAnalyzer = FlowAnalyzer(gsm["flows"]["MSSCEB1B"])

  def test_getLatestClosedIntervalTime(self):
    testCases = [
      ("02.02.2017 15:35:03", "02.02.2017 15:00:00"),
      ("02.02.2017 18:03:00", "02.02.2017 17:30:00"),
      ("02.02.2017 01:00:00", "02.02.2017 00:30:00"),
      ("02.02.2017 00:15:03", "01.02.2017 23:30:00"),
      ("02.02.2017 00:00:00", "01.02.2017 23:30:00"),
      ("01.02.2017 23:59:59", "01.02.2017 23:00:00"),
    ]
    for testCase in testCases:
      latestClosedIntervalTime = self.lobAnalyzer._getLatestCompleteTicTime(util.stringToTime(testCase[0]))
      self.assertEqual(latestClosedIntervalTime, util.stringToTime(testCase[1]))


if __name__ == '__main__':
  unittest.main()
