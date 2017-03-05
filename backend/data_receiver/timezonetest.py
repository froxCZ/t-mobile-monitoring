import pytz
from bson import CodecOptions

import data_receiver.util as util

dateTime = util.stringToDate("30.10.16 02:56:05").replace(tzinfo=pytz.timezone('CET'))

print(dateTime)

from mongo import mongo

x = mongo.lobs().with_options(
  codec_options=CodecOptions(
  tz_aware=True,
  tzinfo=pytz.timezone('CET'))).find_one()
print(x)