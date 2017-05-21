import unittest

import util
from mediation.flow_analyzer import FlowAnalyzer

"""
Class for testing that flow analyzer is using most recent but complete tick time, including DST change.
"""


class TickTest(unittest.TestCase):
  def setUp(self):
    self.flow = {'lobName': 'GSM', 'type': 'inputs', 'dataPath': 'CZ.GSM.inputs.MSSCEB1B', 'name': 'MSSCEB1B',
                 'gName': 'CZ_GSM_MSSCEB1B',
                 'options': {'difference': 'day', 'hardAlarmLevel': 0.5, 'minimalExpectation': 1, 'enabled': True,
                             'lazyDayDifference': 0.7, 'granularity': 60, 'softAlarmLevel': 0.75}, 'country': 'CZ'}

  def test_getLatestCompleteTickTime(self):
    self.flow["options"]["granularity"] = 30
    lobAnalyzer = FlowAnalyzer(self.flow)
    testCases = [
      ("02.02.2017 15:35:03", "02.02.2017 15:00:00"),
      ("02.02.2017 18:03:00", "02.02.2017 17:30:00"),
      ("02.02.2017 01:00:00", "02.02.2017 00:30:00"),
      ("02.02.2017 00:15:03", "01.02.2017 23:30:00"),
      ("02.02.2017 00:00:00", "01.02.2017 23:30:00"),
      ("01.02.2017 23:59:59", "01.02.2017 23:00:00")
    ]
    for testCase in testCases:
      latestCompleteTickTime = lobAnalyzer._getLatestCompleteTicTime(util.stringToTime(testCase[0]))
      self.assertEqual(latestCompleteTickTime, util.stringToTime(testCase[1]))

  def test_getLatestCompleteTickTimeOnDST(self):
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
    for testCase in testCases:
      self.flow["options"]["granularity"] = testCase[2]
      lobAnalyzer = FlowAnalyzer(self.flow)
      latestClosedIntervalTime = lobAnalyzer._getLatestCompleteTicTime(util.stringToTime(testCase[0]))
      expected = util.stringToTime(testCase[1])
      self.assertEqual(latestClosedIntervalTime, expected)


if __name__ == '__main__':
  unittest.main()
