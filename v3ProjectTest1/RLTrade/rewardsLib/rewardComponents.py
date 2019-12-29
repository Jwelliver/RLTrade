"""
    12/22/19
    rewardComponents.py

        -modular reward functions which include the metadata format
        -rewards must return float
        -all component funcs must include 'getMetadata' param, which is a dict with at least {'name': "", 'desc': ""}
            - 'name': general short string that may be used as header in dataframe, or graph,, etc.
            - 'desc': general description of the function's return values.
"""


########################
# Position info functions
########################

##### Position info | "onClosed" functions #####

def position_onClosed_userDefined(tradingAccount,positiveReward=0,negativeReward=0,breakEvenReward=None, breakEvenBias='+',default=0, getMetadata=False):
    """ returns positiveReward or negativeReward based on value of position just closed; if breakEvenReward==None, breakevenBias is used to determine whether the pos or neg reward is returned in a breakeven(val==0) position; If no trade was just closed, returns default """ 
    if getMetadata: return {'name': 'position_onClosed_userDefined','desc': 'User-defined Positive/Negative/Breakeven rewards on position just closed; otherwise, returns default value'}
    posJustClosed = tradingAccount.getPositionClosedOnLastBar()
    if posJustClosed !=None: 
        posVal = posJustClosed.getPositionValue()
        if posVal==0 and breakEvenReward!=None: return breakEvenReward
        if breakEvenBias=='-': return positiveReward if posVal > 0 else negativeReward
        return positiveReward if posVal >= 0 else negativeReward
    else: return default

def position_onClosed_posValue(tradingAccount,default=0, getMetadata=False):
    """ returns value of position just closed; otherwise, returns default """
    if getMetadata: return {'name': 'position_onClosed_posValue','desc': 'Value of the position closed on the previous bar; otherwise, returns default value'}
    posJustClosed = tradingAccount.getPositionClosedOnLastBar()
    if posJustClosed !=None: return posJustClosed.getPositionValue()
    else: return default

def position_onClosed_posValAsPctChangeOfAcc(tradingAccount,default=0, getMetadata=False):
    """ returns value of position just closed as a percent of change in account value; otherwise, returns default """
    if getMetadata: return {'name': 'position_onClosed_posValAsPctChangeOfAcc','desc': 'Value of the position closed on the previous bar; otherwise, returns default value'}
    posJustClosed = tradingAccount.getPositionClosedOnLastBar()
    if posJustClosed !=None: 
        posValue = posJustClosed.getPositionValue()
        accBalBeforeTrade = tradingAccount.accountBalance - posValue
        posValPctOfAcc = posValue / accBalBeforeTrade
        return posValPctOfAcc
    else: return default

##### Position info | "open" functions #####

def position_open_userDefined(tradingAccount,positiveReward=0,negativeReward=0,breakEvenReward=None, breakevenBias='+',default=0, getMetadata=False):
    """ returns positiveReward or negativeReward based on value of position just closed; if breakEvenReward==None, breakevenBias is used to determine whether the pos or neg reward is returned in a breakeven(val==0) position; If no trade was just closed, returns default """ 
    if getMetadata: return {'name': 'position_open_userDefined','desc': 'User-defined Positive/Negative/Breakeven rewards on open position; otherwise, returns default value'}
    curPos = tradingAccount.getCurrentPosition()
    if curPos !=None: 
        posVal = curPos.getPositionValue()
        if posVal==0 and breakEvenReward!=None: return breakEvenReward
        if breakevenBias=='-': return positiveReward if posVal > 0 else negativeReward
        return positiveReward if posVal >= 0 else negativeReward
    else: return default

def position_open_posValue(tradingAccount,default=0,getMetadata=False):
    """ returns value of currently open position; otherwise, returns default """
    if getMetadata: return {'name': 'position_open_posValue','desc': 'Value of the currently open position; otherwise, returns default value'}
    if tradingAccount.hasOpenPosition(): return tradingAccount.getCurrentPositionValue()
    else: return default


########################
# Account info functions
########################

def account_allTimePL(tradingAccount, getMetadata=False):
    """ returns total PL for the account """
    if getMetadata: return {'name': 'account_allTimePL','desc': 'Total PL'}
    return tradingAccount.accountBalance - tradingAccount.initialBalance


def account_allTimePL_asPctChangeOfAcc(tradingAccount, getMetadata=False):
    """ returns total PL for the account as percent of init acc bal"""
    if getMetadata: return {'name': 'account_allTimePL','desc': 'Total PL as pct of initial account balance'}
    return (tradingAccount.accountBalance - tradingAccount.initialBalance) /tradingAccount.initialBalance