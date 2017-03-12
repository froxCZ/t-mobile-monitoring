import api.util as util
import matplotlib.pyplot as plt

from mediation.api.data_query import DateRangeGroupQuery

fromDate = util.jsStringToDate("2016-10-24T00:00:00.000Z")
toDate = util.jsStringToDate("2016-10-31T00:00:00.000Z")
q = DateRangeGroupQuery(fromDate, toDate, ["CZ.SMS"], 5)
lob1Data, metricsList = q.execute()
lob1Data = util.dateDataListToList(lob1Data, metricsList[0])


import pandas, numpy as np
ewma = pandas.stats.moments.ewma

# make a hat function, and add noise
x = np.linspace(0,1,100)
x = np.hstack((x,x[::-1]))
x += np.random.normal( loc=0, scale=0.1, size=200 )
x= np.array(lob1Data)
plt.plot( x, alpha=0.4, label='Raw' )

# take EWMA in both directions with a smaller span term
fwd = ewma( x, span=5 ) # take EWMA in fwd direction
bwd = ewma( x[::-1], span=5 ) # take EWMA in bwd direction
c = np.vstack(( fwd, bwd[::-1] )) # lump fwd and bwd together
c = np.mean( c, axis=0 ) # average

# regular EWMA, with bias against trend
plt.plot( ewma( x, span=20 ), 'b', label='EWMA, span=20' )

# "corrected" (?) EWMA
plt.plot( c, 'r', label='Reversed-Recombined' )
import smooth
plt.plot( smooth.smoothData(15,lob1Data), 'g', label='Smooth' )

plt.legend(loc=8)
#savefig( 'ewma_correction.png', fmt='png', dpi=100 )
plt.show()
