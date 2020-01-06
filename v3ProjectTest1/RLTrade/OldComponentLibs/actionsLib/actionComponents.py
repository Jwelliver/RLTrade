"""
    12/22/19
    actionComponents.py

        -modular action functions which include the metadata format
        -all component funcs must include 'getMetadata' param, which is a dict with at least {'name': "", 'desc': ""}
            - 'name': general short string that may be used as header in dataframe, or graph,, etc.
            - 'desc': general description of the function's return values.
"""

####################
# Entry and Exits
####################


def doNothing(getMetadata=False):
    """ take no action """
    if getMetadata: return {'name': 'doNothing', 'desc': 'Take no action.'}
    pass

def enterLong(tradingAccount, getMetadata=False):
    """ attempt to enter long position """
    if getMetadata: return {'name': 'enterLong', 'desc': 'Attempt to enter long position'}
    tradingAccount.enterPosition(orderType='buy', allowExit=False)

def enterShort(tradingAccount, getMetadata=False):
    """ attempt to enter short position """
    if getMetadata: return {'name': 'enterShort', 'desc': 'Attempt to enter short position'}
    tradingAccount.enterPosition(orderType='sell', allowExit=False)

def enterLong_exitShort(tradingAccount, getMetadata=False):
    """ attempt to enter new long position or exit an existing short position """
    if getMetadata: return {'name': 'enterLong_exitShort', 'desc': 'Attempt to enter long or exit existing short'}
    tradingAccount.enterPosition(orderType='buy', allowExit=True)

def enterShort_exitLong(tradingAccount, getMetadata=False):
    """ attempt to enter new short position or exit an existing long position """
    if getMetadata: return {'name': 'enterShort_exitLong', 'desc': 'Attempt to enter short or exit existing long'}
    tradingAccount.enterPosition(orderType='buy', allowExit=True)

def exitCurrentPosition(tradingAccount, getMetadata=False):
    """ exit the current position if one exists """
    if getMetadata: return {'name': 'exitPosition', 'desc': 'Exit current position.'}
    tradingAccount.exitPosition()

####################
# Position Sizing
####################

def increasePositionSize(tradingAccount, positionSizeIncrement, getMetadata=False):
    """ increase position size by positionSizeIncrement  """
    if getMetadata: return {'name': 'increasePositionSize', 'desc': 'Increase position size'}
    tradingAccount.adjustPositionSize(positionSizeIncrement)

def decreasePositionSize(tradingAccount, positionSizeIncrement, getMetadata=False):
    """ decrease position size by positionSizeIncrement  """
    if getMetadata: return {'name': 'decreasePositionSize', 'desc': 'Decrease position size'}
    positionSizeIncrement = -abs(positionSizeIncrement) # ensure correct sign
    tradingAccount.adjustPositionSize(positionSizeIncrement)