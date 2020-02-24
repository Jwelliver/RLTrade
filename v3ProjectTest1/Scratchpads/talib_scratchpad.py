# Josh: dl ta-lib from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib 
# ... make sure to get proper version, "cp38" means python 3.8
# then pip install through cmd prompt
import talib
from talib.abstract import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Cursor, MultiCursor
from RLTrade.assetTestData import assetDataLib


#--Setup TestAsset data
testData = assetDataLib.baseLineData0(tickDataSize=560) #560=100 bars |  #2560 = 500 bars
#print(testData)
#testData*=10
#print(testData)

#--talib Abstract approach
smaTestFunc = talib.abstract.Function('sma') # alternatively, can use abstract.SMA

smaData_abstract = smaTestFunc(testData,timeperiod=3)
#print(smaData_1)

#--talib Function approach
smaData1 = talib.SMA(testData['close'],timeperiod=3)
smaData2 = talib.SMA(testData['close'],timeperiod=5)

linRegSlope1 = talib.LINEARREG_SLOPE(smaData1, timeperiod=3)
linRegSlope2 = talib.LINEARREG_SLOPE(smaData1, timeperiod=5)

linRegSlope3 = talib.LINEARREG_SLOPE(smaData2, timeperiod=3)
linRegSlope4 = talib.LINEARREG_SLOPE(smaData2, timeperiod=5)

rsi1 = talib.RSI(linRegSlope1)
rsi2 = talib.RSI(linRegSlope2)

stoch1_k, stoch1_d = talib.STOCH(linRegSlope1,linRegSlope1,linRegSlope1)

stochRsi1_k, stochRsi1_d = talib.STOCHRSI(linRegSlope1,timeperiod=7)

#print(testData)

#-- plot tests


"""
fig, axs = plt.subplots(3)
axs[0].plot(testData['close'])
axs[0].plot(smaData1)
axs[0].plot(smaData2)
axs[1].plot(testData.index.values, linRegSlope1, color='k')
axs[1].plot(testData.index.values, linRegSlope2)
axs[2].plot(testData.index.values, linRegSlope3, color='k')
axs[2].plot(testData.index.values, linRegSlope4)
"""

ax1 = plt.subplot(511)
ax1.plot(testData['close'])
ax1.plot(smaData1)
ax1.plot(smaData2)

ax2 = plt.subplot(512,sharex=ax1)
ax2.plot(testData.index.values, linRegSlope1, color='k')
ax2.plot(testData.index.values, linRegSlope2)

ax3 = plt.subplot(513,sharex=ax1)
ax3.plot(testData.index.values, rsi1, color='k')
ax3.plot(testData.index.values, rsi2)

ax4 = plt.subplot(514,sharex=ax1)
ax4.plot(testData.index.values, stoch1_k, color='k')
ax4.plot(testData.index.values, stoch1_d)

ax5 = plt.subplot(515,sharex=ax1)
ax5.plot(testData.index.values, stochRsi1_k, color='k')
ax5.plot(testData.index.values, stochRsi1_d)

"""ax3 = plt.subplot(313,sharex=ax1)
ax3.plot(testData.index.values, linRegSlope3, color='k')
ax3.plot(testData.index.values, linRegSlope4)"""

#cursor = Cursor(ax1, useblit=True, color='red', linewidth=1)
multiCursor = MultiCursor(plt.gcf().canvas,(ax1,ax2,ax3, ax4, ax5), color='r', lw=1)

plt.show()