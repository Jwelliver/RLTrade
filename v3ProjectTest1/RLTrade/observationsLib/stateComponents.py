"""
    12/22/19
    stateComponents.py

        modular feature functions which include the metadata format

        -all component funcs must include 'getMetadata' param, which is a dict with at least {'name': "", 'desc': ""}
            - 'name': general short string that may be used as header in dataframe, or graph,, etc.
            - 'desc': general description of the function's return values.
"""

########################
# Trader info functions
########################


def trader_positionStatus(tradingAccount, getMetadata=False):
    """ returns trader position status """
    if getMetadata: return {'name': 'PositionStatus','desc': 'Position status of trading account'}
    return tradingAccount.getPositionStatus()

def trader_currentPositionValueAsPctOfAccountBalance(tradingAccount, getMetadata=False):
    """ returns value of currently open position as percent of account balance(i.e. realized PL) """
    if getMetadata: return {'name': 'CurrentPositionVal_pctOfAccountBal','desc': 'Current position value as a percent of account balance'}
    return (tradingAccount.getCurrentPositionValue() / tradingAccount.accountBalance)

def trader_marginReqAsPctOfAccVal(tradingAccount, getMetadata=False):
    """ returns the current margin requirement for the current position size as a percent of the AccountValue (w/ unrealized PL) """
    if getMetadata: return {'name': 'MarginReq_pctOfAccountVal','desc': 'current margin requirement for the current position size as a percent of the AccountValue (w/ unrealized PL)'}
    return (tradingAccount.positionSize * tradingAccount.marginRequirement) / tradingAccount.getAccountValue()

########################
# Asset info functions
########################

def asset_getActiveAssetFeatures(tradingAccount, featuresList, getMetadata=False): #this will probably need to be replaced by less-abstract functions
    """ returns list of features """
    if getMetadata: return {'name': 'market_getActiveAssetFeatures','desc': 'List of Features from the active asset'}
    return tradingAccount.market.getAssetDataFeatures([tradingAccount.activeAssetId],featuresList)

def asset_is6smaAboveClose(tradingAccount, getMetadata=False):
    """ returns 1 if 7smam > close price; otherwise, 0 """
    assetData = tradingAccount.market.getData(tradingAccount.activeAssetId)
    return int(assetData['sma6'] > assetData['c'])

def asset_is6smaAbove12sma(tradingAccount, getMetadata=False):
    """ returns 1 if 7smam > close price; otherwise, 0 """
    assetData = tradingAccount.market.getData(tradingAccount.activeAssetId)
    return int(assetData['sma6'] > assetData['sma12'])