import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import plotly.graph_objects as pltgo
import datetime

def getDateTimeIndex(length, startDate="01/01/19", timeIntervalInSec=1):
    """ returns dummy dt index for pandas dataframes """
    timeData = []
    dt = datetime.datetime.strptime(startDate,'%m/%d/%y')
    timeDelta = datetime.timedelta(seconds=timeIntervalInSec)
    for i in range(length):
        timeData.append(dt.strftime("%m/%d/%y %H:%M:%S"))
        dt += timeDelta
    return pd.DatetimeIndex(pd.to_datetime(timeData).values)

def getSineData(nDatapoints,baseNumber=10, smoothing=10):
    """ returns nDatapoints sine data beginning from baseNumber(acts as offset); smoothing is a pseudo-frequency value - the higher the smoothing, the bigger the waves are over nDatapoints. it was born out of poor math skills"""
    start,end = 0,nDatapoints/smoothing
    interval = (end-start)/nDatapoints
    x = np.arange(start,end,interval)
    y = [i + baseNumber for i in np.sin(x)]
    return x,y

def getSineTickData(nDatapoints, basePrice=10, smoothing = 10, baseDate="01/01/19",timeIntervalInSec=1):
    """ returns nDatapoints of dummy price series data as a Series """
    x,y = getSineData(nDatapoints,basePrice,smoothing)
    dtIndex = getDateTimeIndex(len(y),baseDate,timeIntervalInSec)
    return pd.DataFrame(y,index=dtIndex,dtype='float64')[0]

def getOhlcDataFromTickData(tickDataDf, periodInSeconds=300, ohlc_colNames = None):
    """ coverts tickData dataframe into OHLC data at the specified period. """
    ohlc = tickDataDf.resample(str(periodInSeconds)+'S').ohlc()
    if ohlc_colNames != None:
        ohlc.columns = ohlc_colNames
    return ohlc

def getOhlcSineData(nTickDatapoints, basePrice=10, smoothing = 10, baseDate="01/01/19",tickTimeIntervalInSeconds=1,candlePeriodInSeconds=300, colnames = ['o','h','l','c'], datesAsColumn = False):
    """ generates nTickDatapoints worth of sinewave data, then converts and returns it as ohlc data for testing """
    tickData = getSineTickData(nTickDatapoints,basePrice,smoothing,baseDate,tickTimeIntervalInSeconds)
    ohlc = getOhlcDataFromTickData(tickData,candlePeriodInSeconds,colnames)
    if datesAsColumn:
        ohlc['date'] = ohlc.index.values
    return ohlc

def getSMA(series, period=14):
    """ returns a pandas Series of Simple moving average data from the given series """
    s = pd.Series(series)
    #df['sma_'+str(period)] = 
    return s.rolling(window=period).mean()

def getDifferenceBetweenSeries(seriesA,seriesB):
    """ takes 2 series and returns a new series which contains the difference between seriesA and seriesB (b-a); e.g. a=[2,2,3,4], b=[3,4,5,6] -> [1,2,2,2] """
    t = []
    l = np.amax(len(seriesA),len(seriesB))
    for i in range(l):
        t.append(seriesB[i] - seriesA[i])
    return t

def getFXSineTickData_pct(nDataPoints,smoothing=10, baseFxPrice = 1.0000, basePip = 0.0010 ):
    """ returns better quality sine tick data by performing some operations on the output of getSineTickData() """
    # applies pct change in each SineTick to pct of 20 pips, then applies the difference to 
    t = getSineTickData(nDataPoints,1.1,smoothing)
    pctChange = pd.Series(t).pct_change()
    d = [baseFxPrice]
    for i in pctChange[1:].values:
        nextPrice = d[-1] + (basePip * i)
        d.append(nextPrice)
    return d

def getFXSineTickData_linear(nDataPoints,smoothing=10, baseFxPrice = 1.0000, basePip = 0.0001 ):
    """ returns better quality sine tick data by performing some operations on the output of getSineTickData() """
    # converts positive and negative movements of sine tick data to output
    t = getSineTickData(nDataPoints,1.1,smoothing)
    pctChange = pd.Series(t).pct_change()
    d = [baseFxPrice]
    for i in pctChange[1:].values:
        nextPrice = basePip if (i >= 0) else -basePip
        d.append(d[-1] + nextPrice)
    return d

def getFXSineTickData_squash(nDataPoints,smoothing=10, baseFxPrice = 1.0000, squashing = 100, noise = 0.001):
    """ returns better quality sine tick data by performing some operations on the output of getSineTickData() """
    # divides SineTick data by squashing value
    t = getSineTickData(nDataPoints,1.1,smoothing) / squashing
    d = [baseFxPrice]
    diff = [t[i-1] - t[i] for i in range(1,len(t))]
    for i in diff:
        nextPrice = d[-1] + i
        d.append(nextPrice)
    d = pd.Series(d,index=getDateTimeIndex(len(d)))
    d += np.random.normal(0,noise,nDataPoints)
    return d

def shiftArray(a,nShift, keepSize=True):
    """  shifts data in a nShift places to the right(positive nShift) or left(nShift); if keepSize is True, the shifted values will be replaced with None"""
    #heads up - You can just use panda's built in series shift
    t = np.roll(a,nShift)
    t = t[nShift:] if nShift>0 else t[:-abs(nShift)]
    if(keepSize):
        padPlacement = (nShift,0) if nShift>0 else (0,abs(nShift))
        t = np.pad(t,padPlacement)
    return t


# testing ----------------



#t = getFXSineTickData_squash(1000,smoothing=20,squashing=100)
#p = getOhlcDataFromTickData(t,5)

#t = getSineTickData(100)/1000

#print(t)
#print(p)

#plt.plot(t)
#plt.show()

'''
for i in range(1,11):
    print("i: {}".format(i))
    x,t = getSineData(100,1.1,i)
    d = t[1] - t[0]
    da = [t[i-1] - t[i] for i in range(1,len(t))]
    print('t: \n {} \n\n da: {} \n d: {}'.format(t,da,d))
'''
#print(getDifferenceBetweenSeries(a,b))

#d = [5,2,3,4,5,6,7,8,9,10]
#print(getSMA_old(d,4))

#df = pd.DataFrame(d)
#print(df)
#print(getSMA(d,3))

#ohlcDataframe = getOhlcSineData(100,basePrice=1)
#ohlcDictArray = ohlcDataframe.to_dict('records') #converts to a dictArray
#maData = getSMA(ohlcDataframe['c'],26)

#print(maData)

#ohlcDataframe['ma'] = maData
#print(ohlcDataframe)
#print(ohlcDictArray)



#tickData = getSineTickData(100,timeIntervalInSec=30)
#ohlcData = getOhlcDataFromTickData(tickData,periodInSeconds=300)

#print(ohlcData.to_dict('records'))

#rangeData = ohlcData.set_index(pd.RangeIndex(stop=len(ohlcData)))
#print(rangeData['open'][0])

#fig = pltgo.Figure(data=pltgo.Candlestick(x=ohlcData.index.values, open=ohlcData[0]['open'],high=ohlcData[0]['high'],low=ohlcData[0]['low'],close=ohlcData[0]['close']))
#fig.show()



'''
#print(getSineTickData(10,getAsSeparateLists=True))


x,y = getSineTickData(100,getAsSeparateLists=True)
#print(len(x))

plt.plot(x,y)
plt.show()

'''

'''
110219

need to test run the system with sinwave data.
above is a way to generate such data..
need to convert it into OHLC - eg. https://blog.quantinsti.com/tick-tick-ohlc-data-pandas-tutorial/
probably also want to add the MA distance value, which can be done with ta-lib

once the test data is ready, need to finish prepping main_1.py for use with our environment
-only needs a tiny bit of tweaking

we also need a way to visualize the training results.. at first, we could probably just plot or print the account balance, or value .. but would ultimately be nice to view trades against price data

you can then start running the system on the test data to work out any issues

---

As of today, I felt 100% less comfortable and sure than I did on the day I desined the system and implemented 99% of it.
-When I left the project a few weeks ago, I felt within minutes of completing enough for the first MVP test.. today, I coudld not get a solid overview of everything in my mind.
I would feel better going over everything again, and documenting the thought process - and possibly overhauling the system.
One thing that needs to be done is making sure environment variables (features, rewards, etc) have an easy interface to be modular and swapped in/out.

110319:

-Just need to figure out how to get the MA data for the env feature before testing can start.
I can just build an SMA thing, but have been trying to figure out how to do it with a dataframe.. https://www.datacamp.com/community/tutorials/moving-averages-in-pandas
but it's getting late

110919:

Looks like the dataframe sma approach "not working" was actually just you being a sleepy imbecile (also, you couldn't even spell that correctly!!.. :) )
The output was correct. Just verified by building a manual getSMA method and hand calc.







'''


'''
#removed functions:

def getSMA_manual(series, period=14):
    """ returns a list of SMA data using the given from the given series """
    smaData = [None for i in range(period)]
    for i in range(period,len(series)):
        avgChunk = series[i-period:i]
        avg = sum(avgChunk)/period
        smaData.append(avg)
    return smaData

'''