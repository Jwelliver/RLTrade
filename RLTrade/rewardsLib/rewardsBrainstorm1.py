"""
    11/30/19
    RewardsBrainstorm1

    This module will act as a container for various reward functions during development/testing
"""

def baseline1(tradingAccount):
    """ baseline reward - 0 if no position; -1 if positionValue is negative; 1 if positionValue is positive"""
    reward = 0
    if tradingAccount.hasOpenPosition():
        reward = 1 if tradingAccount.currentTrade.getPositionValue(tradingAccount.getCurrentOHLC()['c']) > 0 else -1
    return reward

def baseline2(tradingAccount):
    """ Not in pos: -0.5; in winning pos: +0.2; in losing pos: -0.2; closed winning pos: +1 + %gain; closed losing pos: -1 - %loss """
    posJustClosed = tradingAccount.getPositionClosedOnLastBar()
    if posJustClosed !=None:
        posValue = posJustClosed.getPositionValue()
        accBalBeforeTrade = tradingAccount.accountBalance - posValue
        posValPctOfAcc = posValue / accBalBeforeTrade
        reward = 0.2 if posValue > 0 else -0.2
        return reward + posValPctOfAcc # reward for closing a position

    if tradingAccount.hasOpenPosition():
        return 0.2 if tradingAccount.getCurrentPositionValue() > 0 else -0.2 # currently in winning or losing/breakeven pos
    else:
        return -0.0 #Not in pos
    return -99999 # return catchall - may want to change this to 0 after testing