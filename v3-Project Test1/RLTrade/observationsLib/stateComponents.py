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
    return (self.tradingAccount.getCurrentPositionValue() / self.tradingAccount.accountBalance)

def trader_marginReqAsPctOfAccVal(tradingAccount, getMetadata=False):
    """ returns the current margin requirement for the current position size as a percent of the AccountValue (w/ unrealized PL) """
    if getMetadata: return {'name': 'MarginReq_pctOfAccountVal','desc': 'current margin requirement for the current position size as a percent of the AccountValue (w/ unrealized PL)'}
    return (self.trader.positionSize * self.trader.marginRequirement) / self.trader.getAccountValue()

########################
# Asset info functions
########################


