"""
    120119 - TradingAccount Class
    
    Contains trading account information and handles trade management.
"""

import pandas as pd
from TradePosition import TradePosition

class TradingAccount():
    def __init__(self,marketObj,initialBalance,marginRequirement=0.05,enableCommission=True, positionSize=1000):
        self.initialBalance = initialBalance
        self.accountBalance = self.initialBalance
        self.marginRequirement = marginRequirement
        self.enableCommission = enableCommission
        self.activeAssetId = 0 #this is the asset that actions will be applied to 
        self.positionSize = positionSize
        self.positions = [] # list of TradePosition objects
        self.accountLog = pd.DataFrame()
        self.market = marketObj
        self.marginFlag = 0
    


        ##################
        # ACCOUNT METHODS
        ##################

    def adjustBalance(self,adjustment):
        """ adjusts account balance by adjustment """
        self.accountBalance += adjustment

    def getAccountValue(self, includeUnrealizedPL=False):
        """ returns account value; if includeUnrealizedPL, then open position values are included in the total """
        return (self.accountBalance + self.getUnrealizedPL()) if includeUnrealizedPL else self.accountBalance

    def getUnrealizedPL(self):
        """ returns net value of open positions (this class only handles single trades)"""
        pos = self.getCurrentPosition()
        return 0 if pos==None else pos.getPositionValue()

    def checkMargin(self):
        """ returns a true if margin requirements are met. Check this before opening a trade; and check during a trade for margin calls"""
        marginRequirementValue = self.positionSize * self.marginRequirement
        accVal = self.getAccountValue()
        sufficientMargin = False
        if self.hasOpenPosition():
            assetDataCurBar = self.market.getData(self.activeAssetId)
            accValueAtLow = accVal + self.getCurrentPosition().getPositionValue(price=assetDataCurBar['l'])
            accValueAtHigh = accVal + self.getCurrentPosition().getPositionValue(price=assetDataCurBar['h'])
            sufficientMargin = (accValueAtLow > marginRequirementValue and accValueAtHigh > marginRequirementValue)
            if not sufficientMargin: self.marginFlag = 3 #margin call would have occurred during last candle
        else:
            sufficientMargin = (accVal > marginRequirementValue)
            if not sufficientMargin: self.marginFlag = 2 #insufficient margin to open a new trade
        return sufficientMargin


        #############################
        # POSITION MODIFY METHODS
        #############################

    def handleMarginCall(self):
        """ handles margin call activity """
        self.exitPosition()

    def enterPosition(self, orderType="buy"):
        """ handles new position - if a trade is already open and is the opposite orderType, that trade will be closed; If an open trade in the same direction exists, or orderType=None, no action is taken"""
        if orderType == None:
            return
        if not self.hasOpenPosition() and self.checkMargin():
            activeAsset = self.market.getAsset(self.activeAssetId)
            self.positions.append(TradePosition(activeAsset,orderType,self.positionSize,activeAsset.getClosePrice(),entryBarNum=self.market.currentBarNum,enableCommission=self.enableCommission))
        elif self.getCurrentPosition().orderType != orderType:
            self.exitPosition()

    def exitPosition(self):
        """ exits current position, if any"""
        curPos = self.getCurrentPosition()
        if(curPos==None): return False
        curPos.closePosition()
        self.adjustBalance(curPos.getPositionValue())

        #############################
        # POSITION INFO METHODS
        #############################

    def hasOpenPosition(self):
        """ returns true if an open position exists, else None"""
        return None if len(self.positions) < 1 else self.positions[-1].isActive()
    
    def getCurrentPosition(self):
        """ returns current position object if one exists, else return None"""
        return None if not self.hasOpenPosition() else self.positions[-1]

    def getCurrentPositionValue(self):
        """ returns current position value """
        return self.getUnrealizedPL()

    def getPositionStatus(self):
        """ returns 0 if not in a position, 1 if in a long position, 0.5 if in a short position """
        curPos = self.getCurrentPosition()
        if curPos == None: return 0
        else: return 1 if curPos.orderType == 'buy' else 0.5

    def getPositionOpenedOnLastBar(self):
        """ if a position was opened on the previous bar, the TradePosition is returned, otherwise None"""
        wasTradeOpenedLastBar = (self.hasOpenPosition() and self.positions[-1].entryBarNum == self.market.currentBarNum-1)
        return self.positions[-1] if wasTradeOpenedLastBar else None

    def getPositionClosedOnLastBar(self):
        """ if a position was closed on the previous bar, the TradePosition is returned, otherwise None"""
        wasTradeClosedLastBar = (len(self.positions)>0 and self.positions[-1].exitBarNum == self.market.currentBarNum-1)
        return self.positions[-1] if wasTradeClosedLastBar else None
    
        #############################
        # META METHODS
        #############################

    def updateAccountLog(self):
        """ records account info at currentBarNum """
        curBar = market.currentBarNum
        self.accountLog.loc[curBar,'realizedPL'] = self.getAccountValue()
        self.accountLog.loc[curBar,'unrealizedPL'] = self.getAccountValue(includeUnrealizedPL=True)
        self.accountLog.loc[curBar,'nTrades'] = len(self.positions)
        self.accountLog.loc[curBar,'positionStatus'] = self.getPositionStatus()
        self.accountLog.loc[curBar,'marginFlag'] = self.marginFlag

    def reset(self):
        """ reinits self """
        self.__init__(self.market,self.initialBalance,self.marginRequirement,self.enableCommission)





''' #Unused methods
def getUnrealizedPL(self): #save this for multiTrade capability - while copying to 120119, sticking with single trade approach for time (and training speed)
    """ returns net value of open positions """
    unrealizedPl = 0
    for i in self.positions:
        if i.isActive(): unrealizedPl+=i.getPositionValue()
    return unrealizedPl

'''