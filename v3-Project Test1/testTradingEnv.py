"""
121219
testTradingEnv.py

Testing subclassing of TradingEnvironment
"""

from RLTrade.environments import TradingEnvironment
from RLTrade.rewardsLib import rewardsBrainstorm1 as rewards

class TestTradeEnv(TradingEnvironment.TradingEnvironment):
    def __init__(self, **kwds):
        super().__init__(**kwds)
    
    def getStateObservation(self):
        """ returns current observation """
        observation = []
        currentBarNum = self.market.currentBarNum
        #observation.extend(self.envFeatureData[currentBarNum])
        #observation.extend(self.market.getAssetDataFeatures([self.trader.activeAssetId],['sma6_c_diff','sma6_c_diff_prev','sma12_c_diff','sma12_c_diff_prev']))
        observation.extend(self.market.getAssetDataFeatures([self.trader.activeAssetId],['sma6_sma12_diff_delta_from_prev']))
        observation.append(self.trader.getPositionStatus())
        observation.append(self.trader.getCurrentPositionValue() / self.trader.accountBalance) #current Position as pct of accountBal
        #print("TradeEnv1.getStateObservation() > ", observation)
        #baseLine1 = observationsLib.baseline1(self.tradingSim)
        #observation.append(baseLine1)
        return observation

    def getRewardDict(self):
        """ returns the current reward for each eventFlag - You can set eventFlags in self.getEventFlag() """
        
        normalReward = rewards.baseline3(self.trader)
        rewardDict = {
            0: normalReward,
            1: normalReward,
            2: -10, 
            3: -10,
        }
        return rewardDict