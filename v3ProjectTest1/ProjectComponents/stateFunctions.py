
########################
# Trader info functions
########################


def trader_positionStatus(env):
    """ returns trader position status """
    return env.tradingAccount.getPositionStatus()

def trader_currentPositionValueAsPctOfAccountBalance(env):
    """ returns value of currently open position as percent of account balance(i.e. realized PL) """
    return (env.tradingAccount.getCurrentPositionValue() / env.tradingAccount.accountBalance)

def trader_marginReqAsPctOfAccVal(env):
    """ returns the current margin requirement for the current position size as a percent of the AccountValue (w/ unrealized PL) """
    return (env.tradingAccount.positionSize * env.tradingAccount.marginRequirement) / env.tradingAccount.getAccountValue()

########################
# Asset info functions
########################

def asset_getActiveAssetFeatures(env, featuresList): #this will probably need to be replaced by less-abstract functions
    """ returns list of features """
    return env.tradingAccount.market.getAssetDataFeatures([env.tradingAccount.activeAssetId],featuresList)

def asset_is6smaAboveClose(env):
    """ returns 1 if 7smam > close price; otherwise, 0 """
    assetData = env.tradingAccount.market.getData(env.tradingAccount.activeAssetId)
    return int(assetData['sma6'] > assetData['c'])

def asset_is6smaAbove12sma(env):
    """ returns 1 if 7smam > close price; otherwise, 0 """
    assetData = env.tradingAccount.market.getData(env.tradingAccount.activeAssetId)
    return int(assetData['sma6'] > assetData['sma12'])