import talib

########################
# Trader info functions
########################


def trader_positionStatus(env):
    """ returns trader position status """
    return env.trader.getPositionStatus()

def trader_currentPositionValueAsPctOfAccountBalance(env):
    """ returns value of currently open position as percent of account balance(i.e. realized PL) """
    return (env.trader.getCurrentPositionValue() / env.trader.accountBalance)

def trader_marginReqAsPctOfAccVal(env):
    """ returns the current margin requirement for the current position size as a percent of the AccountValue (w/ unrealized PL) """
    return (env.trader.positionSize * env.trader.marginRequirement) / env.trader.getAccountValue()

def trader_positionSize(env):
    """ returns trader's current position size' """
    return env.trader.positionSize

########################
# Asset info functions
########################

def asset_getActiveAssetFeatures(env, featuresList): #this will probably need to be replaced by less-abstract functions
    """ returns list of features """
    return env.trader.market.getAssetDataFeatures([env.trader.activeAssetId],featuresList)

def asset_getClose(env): #asset_getActiveAssetFeatures should be able to get this but I'm getting an error and in a rush
    """ returns close """
    assetData = env.trader.market.getData(env.trader.activeAssetId)
    return assetData['c']

def asset_is6smaAboveClose(env):
    """ returns 1 if 7smam > close price; otherwise, 0 """
    assetData = env.trader.market.getData(env.trader.activeAssetId)
    return int(assetData['sma6'] > assetData['c'])

def asset_is6smaAbove12sma(env):
    """ returns 1 if 7smam > close price; otherwise, 0 """
    assetData = env.trader.market.getData(env.trader.activeAssetId)
    return int(assetData['sma6'] > assetData['sma12'])

########################
# Technical Analysis functions
########################

def ta_rsiOfClose(env, rsiPeriod=5, window=1,multiplier=1):
    """ (ta test func) returns rsi of lcose price"""
    curBar = env.trader.market.currentBarNum
    assetData = env.trader.market.assets[env.trader.activeAssetId].data
    rsi = talib.RSI(assetData['c'], timeperiod=rsiPeriod)
    return rsi[curBar-window:curBar] * multiplier

def ta_linregSlopeOfSma(env, smaPeriod=5,slopePeriod=5, window=1):
    """ (ta test func) returns slope of linreg on 5sma """
    curBar = env.trader.market.currentBarNum
    assetData = env.trader.market.assets[env.trader.activeAssetId].data
    sma = talib.SMA(assetData['c'], timeperiod=smaPeriod)
    linRegSlope = talib.LINEARREG_SLOPE(sma,timeperiod=slopePeriod)
    return linRegSlope[curBar-window:curBar]


def ta_rsiOfLinregSlopeOfSma(env, smaPeriod=5, slopePeriod=5, rsiPeriod=5, window=1, multiplier=1):
    """ (ta test func) returns rsi of slope of linreg on 5sma """
    curBar = env.trader.market.currentBarNum
    assetData = env.trader.market.assets[env.trader.activeAssetId].data
    sma = talib.SMA(assetData['c'], timeperiod=smaPeriod)
    linRegSlope = talib.LINEARREG_SLOPE(sma,timeperiod=slopePeriod)
    rsi = talib.RSI(linRegSlope,timeperiod=rsiPeriod)
    return rsi[curBar-window:curBar] * multiplier