"""
120119
RLTradeController

Acts as interface between agent and trading environment  

"""

from rewardsLib import rewardsBrainstorm1 as rewardsLib
from observationsLib import observationsBrainstorm1 as observationsLib

class RLTradeController():
    def __init__(self, tradingAccount, market):
        self.tradingAccount = tradingAccount
        self.market = market
        self.activeAsset = 0 #not used

    def doAction(self, action):
        ''' performs action on the environment ''' # 0 = do nothing, 1 = buy, 2 = sell
        action = self.getActionDict()[action]
        self.tradingAccount.enterPosition(action)

    def getActionDict(self):
        """ returns dictionary where keys are indexes and values are arbitrary action values which will be used by the doAction() method """
        return { 0: None, 1: 'buy', 2: 'sell'}
    
    def getStateObservation(self):
        ''' returns current state as an observation space object '''
        observation = []
        currentBarNum = self.market.currentBarNum
        #observation.extend(self.envFeatureData[currentBarNum])
        observation.extend(self.getAssetDataFeatures([0],['sma6_c_diff','sma6_c_diff_prev','sma12_c_diff','sma12_c_diff_prev']))
        observation.append(self.tradingAccount.getPositionStatus())
        observation.append(self.tradingAccount.getCurrentPositionValue() / self.tradingAccount.accountBalance) #current Position as pct of accountBal
        #print("TradeEnv1.getStateObservation() > ", observation)
        #baseLine1 = observationsLib.baseline1(self.tradingSim)
        #observation.append(baseLine1)
        return observation

    def getAssetDataFeatures(self,assetIdList,featureKeyList):
        """ returns requested feature values from each asset in assetIdList """
        features = []
        for i in assetIdList:
            for k in featureKeyList:
                features.append(self.market.getData(i,k))
        return features


    def getReward(self):
        """ returns current reward as a float - Uses tradingSim.getStopConditions() to determine reward from the rewardDict. 0,1 are normal reward; 2,3 are margin call/financial ruin"""
        #currentAccVal = self.tradingSim.getAccountValue()
        #previousAccVal = self.tradingSim.accountValueHistory[-2]
        #accValDiff = currentAccVal - previousAccVal
        #pctOfAccountBal = accValDiff / self.tradingSim.accountBalance
        baseline = rewardsLib.baseline2(self.tradingAccount) 
        rewardDict = {
            0: baseline,
            1: baseline,
            2: -10,
            3: -10,
        }
        return rewardDict[self.getStopConditions()]

    def getStopConditions(self):
        """ checks for various stop conditions, and returns a specific int for each condition; if no stop condition is met, returns 0.
        returns:
            0: no stop conditions met
            1: reached end of ohlc data
            2: marginCall
            3: financial ruin / not enough margin to place another trade
        """
        if self.market.currentBarNum >= len(self.market.assets[0].data)-1:
            return 1
        if self.tradingAccount.checkMargin() == False:
            return self.tradingAccount.marginFlag
        return 0

    def reset(self):
        """ handles a reset """
        self.tradingAccount.reset()