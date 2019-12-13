"""
120119
assetDataLib

Contains functions for generating/obtaining asset data
"""
import testDataGeneration as testDataGen
import numpy as np

def baseLineData1():
    """ returns df for testing """

    # - primary ohlc data
    tickData = testDataGen.getFXSineTickData_squash(500,smoothing=20,squashing=100)
    ohlcDataframe = testDataGen.getOhlcDataFromTickData(tickData,periodInSeconds=5,ohlc_colNames=['o','h','l','c'])

    # - set up indicator data here
    ma1_period = 6
    ma1_data = testDataGen.getSMA(ohlcDataframe['c'],ma1_period)
    ma1_c_diff = ohlcDataframe['c'] - ma1_data
    ma1_c_diff_prevBar = ma1_c_diff.shift(1)

    ohlcDataframe['sma6'] = ma1_data
    ohlcDataframe['sma6_c_diff'] = ma1_c_diff
    ohlcDataframe['sma6_c_diff_prev'] = ma1_c_diff_prevBar

    ma2_period = 12
    ma2_data = testDataGen.getSMA(ohlcDataframe['c'],ma2_period)
    ma2_c_diff = ohlcDataframe['c'] - ma2_data
    ma2_c_diff_prevBar = ma2_c_diff.shift(1)

    ohlcDataframe['sma12'] = ma2_data
    ohlcDataframe['sma12_c_diff'] = ma2_c_diff
    ohlcDataframe['sma12_c_diff_prev'] = ma2_c_diff_prevBar

    # - remove bars from the start of the ohlc and indicator data to get rid of incomplete data (e.g. nan values before an MA can begin calculations)
    warmupPeriod = np.amax([ma1_period,ma2_period])
    ohlcDataframe = ohlcDataframe[warmupPeriod:]

    return ohlcDataframe

