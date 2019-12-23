"""
122119
TestTradeEnv_PosSize.py

Testing subclassing of TradingEnvironment - includes variable position sizing
"""

from RLTrade.environments import TradingEnvironment
from RLTrade.rewardsLib import rewardsBrainstorm1 as rewards

class TestTradeEnv_PosSize(TradingEnvironment.TradingEnvironment):
    def __init__(self,positionSizeAdjustmentIncrements=1000, **kwds):
        super().__init__(**kwds)
        self.posSizeIncrements = positionSizeAdjustmentIncrements
    
    def getStateObservation(self):
        """ returns current observation """
        observation = []
        currentBarNum = self.market.currentBarNum
        #observation.extend(self.envFeatureData[currentBarNum])
        #observation.extend(self.market.getAssetDataFeatures([self.trader.activeAssetId],['sma6_c_diff','sma6_c_diff_prev','sma12_c_diff','sma12_c_diff_prev']))
        observation.extend(self.market.getAssetDataFeatures([self.trader.activeAssetId],['sma6_c_diff','sma6_sma12_diff']))
        observation.append(self.trader.getPositionStatus())
        observation.append(self.trader.getCurrentPositionValue() / self.trader.accountBalance) #current Position as pct of accountBal
        #observation.append(self.trader.getCurrentPositionValue() / self.trader.getCurrentPosition().positionSize)
        marginReqAsPctOfVal = (self.trader.positionSize * self.trader.marginRequirement) / self.trader.getAccountValue()
        observation.append(marginReqAsPctOfVal)
        #observation.append(self.trader.getAccountValue())
        #print("TradeEnv1.getStateObservation() > ", observation)
        #baseLine1 = observationsLib.baseline1(self.tradingSim)
        #observation.append(baseLine1)
        #print("getStateObservation() > {}".format(observation))
        return observation

    def getRewardDict(self):
        """ returns the current reward for each eventFlag - You can set eventFlags in self.getEventFlag() """
        normalReward = rewards.baseline5(self.trader)
        endOfEpisodeReward = self.trader.accountBalance - self.trader.initialBalance
        rewardDict = {
            0: endOfEpisodeReward,
            1: endOfEpisodeReward,
            2: -10, 
            3: -10,
        }
        return rewardDict

    def getActionDict(self):
        """ returns dictionary where keys are indexes and values are arbitrary action values which can be used by the doAction() method """
        return { 0: None, 1: 'buy', 2: 'sell', 3: 'incPosSize', 4: 'decPosSize'}

    def doAction(self, action):
        """ performs action on the environment """
        #Default: 0 = do nothing; 1 = Buy; 2 = Sell

        if action==1 or action==2:
            tradeAction = self.getActionDict()[action]
            self.trader.enterPosition(tradeAction)
        
        elif action==3:
            self.trader.adjustPositionSize(self.posSizeIncrements)
        elif action==4:
            self.trader.adjustPositionSize(-self.posSizeIncrements)