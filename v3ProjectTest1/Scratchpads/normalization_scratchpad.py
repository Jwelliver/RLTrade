#022320
#
# for testing approaches to normalization


import numpy as np
import pandas as pd
from sklearn import preprocessing


df = pd.DataFrame(np.random.randn(1,4)* 4 + 3)


def getNewToyDataPoint():
    """ returns single row of new data"""
    return pd.DataFrame((np.random.randn(1,4)* 4 + 3))


def normalizeData(data,df):
    """ normalizes data according to the """
    pass

"""
print(df, "\n===1")
df = df.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)))
print(df, "\n===2")
df = df.append(getNewToyDataPoint())
print(df, "\n===3")
df = df.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)))
print(df, "\n===4")
"""

scaler = preprocessing.MinMaxScaler((0,1))

#print(df)

t = df.values
print(t)

st = scaler.fit_transform(df)
print(st)

for i in range(3):
    print("==== %i" % i)
    newData = getNewToyDataPoint()
    print("NewData: \n%s" % newData)
    newDataScaled = scaler.fit_transform(newData)
    print("NewDataScaled: \n%s" % newDataScaled)
    print(st)
    print("scaler.scale: %s" % scaler.scale_)
    print("scaler.min: %s" % scaler.min_)

#scaledDf = df.apply(lambda x: scaler.fit_transform(x))

#print(scaledDf)