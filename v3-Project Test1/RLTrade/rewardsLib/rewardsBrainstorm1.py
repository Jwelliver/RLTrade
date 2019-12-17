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
    """ reward description: No open positions: -0.5; open winning pos: +0.2; open losing pos: -0.2; onClosing winning pos: +1 + %gain; onClosing losing pos: -1 - %loss """
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

def baseline3(tradingAccount):
    """ no pos: -0.01; inWinning: (posVal/accVal)/nBarsHeld; inLosing: -0.1 + (-0.01*nBarsHeld); onWinClosed: 1 +(posValue/accVal); onLossClosed: -1 + (posVal/accVal) """

    posJustClosed = tradingAccount.getPositionClosedOnLastBar()
    #print('rewardBrainstorm1.baseline3() > barNum: {} '.format(tradingAccount.market.currentBarNum))
    if posJustClosed !=None:
        #print('rewardBrainstorm1.baseline3() > posJustClose !=None ')
        posValue = posJustClosed.getPositionValue()
        accBalBeforeTrade = tradingAccount.accountBalance - posValue
        posValPctOfAcc = posValue / accBalBeforeTrade
        reward = 1 if posValue > 0 else -1
        return reward + posValPctOfAcc # reward for closing a position

    if tradingAccount.hasOpenPosition():
        #print('rewardBrainstorm1.baseline3() > HasOpenPosition() ')
        curPos = tradingAccount.getCurrentPosition()
        posVal = curPos.getPositionValue()
        nBarsHeld = curPos.getAge()
        accBalBeforeTrade = tradingAccount.getAccountValue(False) #tradingAccount.accountBalance - posValue
        #print('rewardBrainstorm1.baseline3() > debug pos 1 | posVal: {} | nBarsHeld: {} | accBalBeforeTrade: {}'.format(posVal,nBarsHeld,accBalBeforeTrade))
        posValPctOfAcc = posVal / accBalBeforeTrade
        #print('rewardBrainstorm1.baseline3() > debug pos 2 | posValPctAcc: {}'.format(posValPctOfAcc))
        return (posValPctOfAcc/nBarsHeld) if curPos.getPositionValue() > 0 else (-0.1 + (-0.01*nBarsHeld)) # currently in winning or losing/breakeven pos
    else:
        return -0.01 #Not in pos

    return -99999 # return catchall - may want to change this to 0 after testing