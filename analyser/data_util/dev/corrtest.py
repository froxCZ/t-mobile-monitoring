from scipy.stats import linregress
lob1Data = [100,200,300]
lob2Data = [1,2,3]
lin = linregress(lob1Data, lob2Data)
print(lin.rvalue)