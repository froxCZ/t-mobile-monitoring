import api.util as util
import matplotlib.pyplot as plt
import numpy as np

from mediation.api.data_query import DateRangeGroupQuery


def running_mean(l, N):
  sum = 0
  result = list( 0 for x in l)

  for i in range( 0, N ):
    sum = sum + l[i]
    result[i] = sum / (i+1)

  for i in range( N, len(l) ):
    sum = sum - l[i-N] + l[i]
    result[i] = sum / N

  return result

fromDate = util.jsStringToDate("2016-10-24T10:00:00.000Z")
toDate = util.jsStringToDate("2016-10-31T10:00:00.000Z")
q = DateRangeGroupQuery(fromDate, toDate, ["CZ.SMS"], 15)
lob1Data, metricsList = q.execute()
lob1Data = util.dateDataListToList(lob1Data, metricsList[0])
sample_time = 0.001
frequency_of_signal  = 5
fft_of_signal_with_noise = np.fft.fft(lob1Data)
f = np.fft.fftfreq(len(fft_of_signal_with_noise),sample_time)

def bandpass_filter(x, freq, frequency_of_signal=frequency_of_signal, band = 0.05):
  if (frequency_of_signal - band) < abs(freq) < (frequency_of_signal + band):
    return x
  else:
    return 0

F_filtered = np.asanyarray([bandpass_filter(x,freq) for x,freq in zip(fft_of_signal_with_noise, f)]);
filtered_signal = np.fft.ifft(F_filtered);

# plt.figure(figsize=(12, 6));
# plt.plot(lob1Data);
# plt.plot(running_mean(lob1Data,10));
# import smooth
# plt.plot(smooth.smoothData(15,lob1Data))
# plt.title('Signal with Noise');
# plt.show()

lob1Data = [0,5,10,15,10,15,10,15,10,15]
plt.figure(figsize=(12, 6));
plt.plot(lob1Data);
plt.plot(running_mean(lob1Data,10));
plt.title('Signal with Noise');
plt.show()