#021920


import talib
from talib.abstract import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Cursor, MultiCursor
from RLTrade.assetTestData import assetDataLib
from RLTrade.visualization.AssetFeaturePlotter import AssetFeaturePlotter
import sklearn as sk
from sklearn import cluster
import pandas as pd


#################################################################
# Get test price data
#################################################################

#--Setup TestAsset data
td = assetDataLib.baseLineData0(tickDataSize=800) #560=100 bars |  #2560 = 500 bars

#################################################################
# Setup indicators
#################################################################

td["smaData1"] = talib.SMA(td['close'],timeperiod=3)

td["smaData2"] = talib.SMA(td['close'],timeperiod=5)

td["linRegSlope1"] = talib.LINEARREG_SLOPE(td["smaData1"], timeperiod=3)
td["linRegSlope2"] = talib.LINEARREG_SLOPE(td["smaData1"], timeperiod=5)

td["linRegSlope3"] = talib.LINEARREG_SLOPE(td["smaData2"], timeperiod=3)
td["linRegSlope4"] = talib.LINEARREG_SLOPE(td["smaData2"], timeperiod=5)

td["rsi1"] = talib.RSI(td["linRegSlope1"])
td["rsi2"]  = talib.RSI(td["linRegSlope2"])

td["stoch1_k"], td["stoch1_d"] = talib.STOCH(td["linRegSlope1"],td["linRegSlope1"],td["linRegSlope1"])

td["stochRsi1_k"], td["stochRsi1_d"] = talib.STOCHRSI(td["linRegSlope1"],timeperiod=7)

td = td.dropna()
#print(td)

#################################################################
# Combine Data for clustering
#################################################################

clusterTrainingData = pd.DataFrame()
clusterTrainingData.set_index = td.index

clusterTrainingData['linRegSlope1'] = td['linRegSlope1']
clusterTrainingData['linRegSlope2'] = td['linRegSlope2']
clusterTrainingData['rsi1'] = td['rsi1']
clusterTrainingData['rsi2'] = td['rsi2']


#print(clusterTrainingData)
clusterTrainingData = clusterTrainingData.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)))
#print(clusterTrainingData)

#print("Done")
#################################################################
#  Clustering
#################################################################

#--Setup Clusterer
cluterer = cluster.AgglomerativeClustering(n_clusters=None,distance_threshold=0.2)
clusterResults = cluterer.fit(clusterTrainingData)
print("nClusters: %d" % (np.amax(clusterResults.labels_)+1))

#################################################################
#  Plot
#################################################################

t = AssetFeaturePlotter()


t.plot( td['close'], td['smaData1'], td['smaData2'], 
        colors=['k'] )

t.plot( td['linRegSlope1'], td['linRegSlope2'],
        colors=['k','b'] )

t.plot( td['rsi1'], td['rsi2'],
        colors=['k','b'] )

t.plot( td['stoch1_k'], td['stoch1_d'],
        colors=['k','b'] )

t.plot( td['stochRsi1_k'], td['stochRsi1_d'],
        colors=['k','b'] )


t.plotClusterLabels(clusterResults.labels_, alpha=0.3)

t.showPlot()