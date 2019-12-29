"""
122219
compoundRewards.py

These reward functions are more complex or specialized and use one or more reward components.
"""

from RLTrade.rewardsLib import rewardComponents

def cr1(tradingAccount, getMetadata=False):
    """ If No open positions: -0.5; open winning pos: +0.2; open losing pos: -0.2; onClosing winning pos: +1 + %gain; onClosing losing pos: -1 - %loss """

    if getMetadata: return {'name': 'CompoundReward1', 'desc': 'No open positions: -0.5; open winning pos: +0.2; open losing pos: -0.2; onClosing winning pos: +1 + %gain; onClosing losing pos: -1 - %loss '}

    noOpenPosition = -0.0
    openPositionPositive = 0.0
    openPositionNegative = -0.1
    onClosePositive = 1
    onCloseNegative = -1

    t = rewardComponents.position_onClosed_posValAsPctChangeOfAcc(tradingAccount,default=None)
    if t != None: return t + (onClosePositive if t>=0 else onCloseNegative)
    return rewardComponents.position_open_userDefined(tradingAccount,positiveReward=openPositionPositive,negativeReward=openPositionNegative,breakEvenReward=0,default=noOpenPosition)

def cr_fixedVals1(tradingAccount, getMetadata=False):
    """ Returns fixed reward for each of the following states: No open positions, open winning pos, open losing pos, onClosing winning pos, onClosing losing pos """

    noOpenPosition = 0.0
    openPositionPositive = 0.0
    openPositionNegative = -0.1
    onClosePositive = 1
    onCloseNegative = -1

    #todo: format the desc below to include the var values
    if getMetadata: return {'name': 'cr_fixedVals1', 'desc': 'No open positions, open winning pos, open losing pos, onClosing winning pos, onClosing losing pos'}

    t = rewardComponents.position_onClosed_posValAsPctChangeOfAcc(tradingAccount,default=None)
    if t != None: return onClosePositive if t>=0 else onCloseNegative
    return rewardComponents.position_open_userDefined(tradingAccount,positiveReward=openPositionPositive,negativeReward=openPositionNegative,breakEvenReward=0,default=noOpenPosition)