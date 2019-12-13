"""
121219
testTradingEnv.py

Testing subclassing of TradingEnvironment
"""

from RLTrade.environments import TradingEnvironment

class TestTradeEnv(TradingEnvironment.TradingEnvironment):
    def __init__(self):
        super().__init__(self)
    
    def getStateObservation(self):
        """ returns current observation """
        observation = []
        currentBarNum = self.market.currentBarNum
        #observation.extend(self.envFeatureData[currentBarNum])
        observation.extend(self.market.getAssetDataFeatures([self.trader.activeAssetId],['sma6_c_diff','sma6_c_diff_prev','sma12_c_diff','sma12_c_diff_prev']))
        observation.append(self.trader.getPositionStatus())
        observation.append(self.trader.getCurrentPositionValue() / self.trader.accountBalance) #current Position as pct of accountBal
        #print("TradeEnv1.getStateObservation() > ", observation)
        #baseLine1 = observationsLib.baseline1(self.tradingSim)
        #observation.append(baseLine1)
        return observation