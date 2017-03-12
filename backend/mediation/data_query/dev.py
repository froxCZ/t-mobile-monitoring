import util
from config import config
from mediation.data_query import DateRangeGroupQuery
from mediation.data_query import DatesQuery
from mediation.data_query import ExpectedTrafficQuery
from mediation.data_query import medianDateRange
from past.data_util import SimilarPastDaysFinder

dates = [util.stringToDate("22.01.2017"), util.stringToDate("02.02.2017")]
gsm = config.getLobConfig("CZ_GSM")
bvs = config.getLobConfig("CZ_BVS")
aci = config.getLobConfig("CZ_ACI")
query = DatesQuery(dates, [gsm["flows"]["MSSBRN1A"]])
res = query.execute()
print(res)

query = DateRangeGroupQuery(dates[0], dates[1], [gsm["flows"]["MSSBRN1A"]])
rangeData = query.execute()
rangeGranularity = query.metadata["granularity"]
print(res)

res = medianDateRange(dates[0], dates[1], [gsm["flows"]["MSSBRN1A"]], rangeGranularity, rangeData)
print(res)

query = ExpectedTrafficQuery(dates[0], [gsm["flows"]["MSSBRN1A"]])
res = query.execute()
print(res)

query = SimilarPastDaysFinder([bvs["flows"]["BVSCTX:CZOPS-BVS"]])
res = query.findSimilarPastDays(dates[0])
print(res)


query = DateRangeGroupQuery(dates[0], dates[1], [config.createMergedFlowsObject("CZ_GSM","forwards")])
rangeData = query.execute()
rangeGranularity = query.metadata["granularity"]
print(rangeData)