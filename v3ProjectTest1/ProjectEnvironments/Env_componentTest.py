"""
122219
Env_componentTest.py

Testing the component system for state/action/rewards
"""

from RLTrade.environments import TradingEnvironment
#from RLTrade.rewardsLib import rewardsBrainstorm1 as rewards
from RLTrade.rewardsLib import rewardComponents as rewards
from RLTrade.rewardsLib import compoundRewards1 as rewards2
from RLTrade.observationsLib import stateComponents as stateFeatures
from RLTrade.actionsLib import actionComponents as actions

class Env_122219(TradingEnvironment.TradingEnvironment):
    def __init__(self,positionSizeAdjustmentIncrements=1000, **kwds):
        super().__init__(**kwds)
        self.posSizeIncrements = positionSizeAdjustmentIncrements
    
    def getStateObservation(self):
        """ returns current observation """
        observation = []
        #observation.extend(stateFeatures.market_getActiveAssetFeatures(self.trader, ['sma6_c_diff','sma6_sma12_diff']))
        observation.append(stateFeatures.asset_is6smaAbove12sma(self.trader))
        observation.append(stateFeatures.asset_is6smaAboveClose(self.trader))
        observation.append(stateFeatures.trader_positionStatus(self.trader))
        #observation.append(stateFeatures.trader_currentPositionValueAsPctOfAccountBalance(self.trader))
        #observation.append(stateFeatures.trader_marginReqAsPctOfAccVal(self.trader))
        observation.append(self.trader.positionSize/10000) # 122419 quick test
        return observation

    def getRewardDict(self):
        """ returns the current reward for each eventFlag - You can set eventFlags in self.getEventFlag() """
        normalReward = rewards.position_onClosed_posValAsPctChangeOfAcc(self.trader)
        endOfEpisodeReward = rewards.account_allTimePL_asPctChangeOfAcc(self.trader)
        rewardDict = {
            0: normalReward,
            1: endOfEpisodeReward,
            2: -1, 
            3: -1,
        }
        return rewardDict

    def getActionDict(self):
        """ returns dictionary where keys are indexes and values are arbitrary action values which can be used by the doAction() method """
        return { 0: None, 1: 'enterLong', 2: 'enterShort', 3: 'exit', 4: 'incPosSize', 5: 'decPosSize'}

    def doAction(self, action):
        """ performs action on the environment """
        #Default: 0 = do nothing; 1 = Buy; 2 = Sell
        if action==1: actions.enterLong(self.trader)
        elif action==2: actions.enterShort(self.trader)
        elif action==3: actions.exitCurrentPosition(self.trader)
        elif action==4: actions.increasePositionSize(self.trader, self.posSizeIncrements)
        elif action==5: actions.decreasePositionSize(self.trader, self.posSizeIncrements)