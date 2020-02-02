########################
# Position info functions
########################

##### Position info | "onClosed" functions #####

def position_onClosed_userDefined(env,positiveReward=0,negativeReward=0,breakEvenReward=None, breakEvenBias='+',default=0):
    """ returns positiveReward or negativeReward based on value of position just closed; if breakEvenReward==None, breakevenBias is used to determine whether the pos or neg reward is returned in a breakeven(val==0) position; If no trade was just closed, returns default """ 
    posJustClosed = env.trader.getPositionClosedOnLastBar()
    if posJustClosed !=None: 
        posVal = posJustClosed.getPositionValue()
        if posVal==0 and breakEvenReward!=None: return breakEvenReward
        if breakEvenBias=='-': return positiveReward if posVal > 0 else negativeReward
        return positiveReward if posVal >= 0 else negativeReward
    else: return default

def position_onClosed_posValue(env,default=0):
    """ returns value of position just closed; otherwise, returns default """
    posJustClosed = env.trader.getPositionClosedOnLastBar()
    if posJustClosed !=None: return posJustClosed.getPositionValue()
    else: return default

def position_onClosed_posValAsPctChangeOfAcc(env,default=0):
    """ returns value of position just closed as a percent of change in account value; otherwise, returns default """
    posJustClosed = env.trader.getPositionClosedOnLastBar()
    if posJustClosed !=None: 
        posValue = posJustClosed.getPositionValue()
        accBalBeforeTrade = env.trader.accountBalance - posValue
        posValPctOfAcc = posValue / accBalBeforeTrade
        return posValPctOfAcc
    else: return default

##### Position info | "while open" functions #####

def position_whileOpen_userDefined(env,positiveReward=0,negativeReward=0,breakEvenReward=None, breakevenBias='+',default=0):
    """ returns positiveReward or negativeReward based on value of currently open position; if breakEvenReward==None, breakevenBias is used to determine whether the pos or neg reward is returned in a breakeven(val==0) position; If no trade was just closed, returns default """ 
    curPos = env.trader.getCurrentPosition()
    if curPos !=None: 
        posVal = curPos.getPositionValue()
        if posVal==0 and breakEvenReward!=None: return breakEvenReward
        if breakevenBias=='-': return positiveReward if posVal > 0 else negativeReward
        return positiveReward if posVal >= 0 else negativeReward
    else: return default

def position_whileOpen_posValue(env,default=0):
    """ returns value of currently open position; otherwise, returns default """
    if env.trader.hasOpenPosition(): return env.trader.getCurrentPositionValue()
    else: return default


########################
# Account info functions
########################

def account_allTimePL(env):
    """ returns total PL for the account """
    return env.trader.accountBalance - env.trader.initialBalance


def account_allTimePL_asPctChangeOfAcc(env):
    """ returns total PL for the account as percent of init acc bal"""
    return (env.trader.accountBalance - env.trader.initialBalance) /env.trader.initialBalance