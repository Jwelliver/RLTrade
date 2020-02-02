
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

########################
# Asset info functions
########################

def asset_getActiveAssetFeatures(env, featuresList): #this will probably need to be replaced by less-abstract functions
    """ returns list of features """
    return env.trader.market.getAssetDataFeatures([env.trader.activeAssetId],featuresList)

def asset_is6smaAboveClose(env):
    """ returns 1 if 7smam > close price; otherwise, 0 """
    assetData = env.trader.market.getData(env.trader.activeAssetId)
    return int(assetData['sma6'] > assetData['c'])

def asset_is6smaAbove12sma(env):
    """ returns 1 if 7smam > close price; otherwise, 0 """
    assetData = env.trader.market.getData(env.trader.activeAssetId)
    return int(assetData['sma6'] > assetData['sma12'])