import unittest

from common import util
from mediation.flow_analyzer import FlowAnalyzer
from mediation.flow_analyzer.status import OK, OUTAGE, WARNING

FLOW = {'lobName': 'GSM', 'type': 'inputs', 'dataPath': 'CZ.GSM.inputs.MSSCEB1B', 'name': 'MSSCEB1B',
        'gName': 'CZ_GSM_MSSCEB1B',
        'options': {'difference': 'day', 'hardAlarmLevel': 0.5, 'minimalExpectation': 1, 'enabled': True,
                    'lazyDayDifference': 0.7, 'granularity': 60, 'softAlarmLevel': 0.75}, 'country': 'CZ'}
CURRENT_TIME = util.stringToTime("17.01.2017 15:03:00")

"""
Class for testing flow analyzer and its results
"""


class FlowAnalyzerTest(unittest.TestCase):
  def setUp(self):
    self.flowAnalyzer = FlowAnalyzer(FLOW)
    self.data = {}
    self.flowAnalyzer.setPrecomputedData(self.data)

  def test_easyOK(self):
    self.addTickToData("17.01.2017 14:00:00", 1000, 50, 100)
    self.assertStatus(OK)

  def test_easyOUTAGE(self):
    self.addTickToData("17.01.2017 14:00:00", 100, 50, 1000)
    self.assertStatus(OUTAGE)

  def test_dayDifferenceOK(self):
    # 10% traffic of expected level, but day average is much more so the outage is not significant
    self.addTickToData("17.01.2017 14:00:00", 100, 10000, 1000)
    self.assertStatus(OK)

  def test_WARNING(self):
    self.addTickToData("17.01.2017 13:00:00", 100, 100, 100)
    self.addTickToData("17.01.2017 14:00:00", 100, 100, 200)
    self.assertStatus(WARNING)

  def test_WARNING_OUTAGE(self):
    # two warnings = OUTAGE
    self.addTickToData("17.01.2017 13:00:00", 100, 100, 200)
    self.addTickToData("17.01.2017 14:00:00", 100, 100, 200)
    self.assertStatus(OUTAGE)

  def assertStatus(self, expectedStatus):
    self.flowAnalyzer.run(CURRENT_TIME)
    self.assertEqual(self.flowAnalyzer.status, expectedStatus)

  def addTickToData(self, tickTime, value, average, expected):
    tick = util.stringToTime(tickTime)
    self.data[tick] = {'_id': tick, 'value': value, 'dayAverage': average, 'expected': expected}


if __name__ == '__main__':
  unittest.main()
