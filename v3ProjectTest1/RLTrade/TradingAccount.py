"""
    120119 - TradingAccount Class
    
    Contains trading account information and handles trade management.
"""

import pandas as pd
from .TradePosition import TradePosition

class TradingAccount():
    def __init__(self,marketObj,initialBalance,marginRequirement=0.05,enableCommission=True, positionSize=1000, name='TradingAcc1'):
        self.name=name
        self.initialBalance = initialBalance
        self.accountBalance = self.initialBalance
        self.marginRequirement = marginRequirement
        self.enableCommission = enableCommission
        self.activeAssetId = 0 #this is the asset that actions will be applied to 
        self.initPositionSize = positionSize
        self.positionSize = self.initPositionSize
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

    def getRealizedPL(self):
        """ return difference in current accountValue(excluding unrealizedPL) from initial value """
        return self.getAccountValue() - self.initialBalance

    def checkMargin(self):
        """ returns a true if margin requirements are met. Check this before opening a trade; and check during a trade for margin calls"""
        marginRequirementValue = self.positionSize * self.marginRequirement
        accVal = self.getAccountValue()
        sufficientMargin = False
        if self.hasOpenPosition():
            curPos = self.getCurrentPosition()
            assetDataCurBar = self.market.getData(self.activeAssetId)
            accValueAtLow = accVal + curPos.getPositionValue(price=assetDataCurBar['l'])
            accValueAtHigh = accVal + curPos.getPositionValue(price=assetDataCurBar['h'])
            sufficientMargin = (accValueAtLow > marginRequirementValue and accValueAtHigh > marginRequirementValue)
            if not sufficientMargin: self.marginFlag = 3 #margin call would have occurred during last candle
        else:
            sufficientMargin = (accVal >= marginRequirementValue)
            if not sufficientMargin: self.marginFlag = 2 #insufficient margin to open a new trade
        return sufficientMargin


        #############################
        # POSITION MODIFY METHODS
        #############################

    def handleMarginCall(self):
        """ handles margin call activity """
        self.exitPosition()

    '''def enterPosition_orig(self, orderType="buy"): # 122219 orig
        """ handles new position - if a trade is already open and is the opposite orderType, that trade will be closed; If an open trade in the same direction exists, or orderType=None, no action is taken"""
        if orderType == None or self.positionSize == 0: return
        if not self.hasOpenPosition() and self.checkMargin():
            activeAsset = self.market.getAsset(self.activeAssetId)
            self.positions.append(TradePosition(activeAsset,orderType,self.positionSize,activeAsset.getClosePrice(),entryBarNum=self.market.currentBarNum,enableCommission=self.enableCommission))
        elif self.getCurrentPosition().orderType != orderType:
            self.exitPosition()'''

    '''def enterPosition_wReversal(self, orderType="buy", allowExit=True, allowReversal=False): #122219: Cannot implement reversal feature until you revise the "getLastTradeClosed" functions to search for last closed trade instead of just searching the most recent index.
        """ handles new position - if a trade is already open with the opposite orderType given: allowExit will exit the current trade while allowReversal will both exit the current trade and enter a new trade in the other direction; If an open trade in the same direction exists, or orderType=None, no action is taken"""
        if orderType == None or self.positionSize == 0: return
        if allowReversal: allowExit=True
        if not self.hasOpenPosition() and self.checkMargin():
            activeAsset = self.market.getAsset(self.activeAssetId)
            self.positions.append(TradePosition(activeAsset,orderType,self.positionSize,activeAsset.getClosePrice(),entryBarNum=self.market.currentBarNum,enableCommission=self.enableCommission))
        elif self.getCurrentPosition().orderType != orderType:
            if allowExit: self.exitPosition()
            if allowReversal: self.enterPosition(orderType)'''

    def enterPosition(self, orderType="buy", allowExit=True):
        """ handles new position - if a trade is already open with the opposite orderType given: allowExit will exit the current trade ; If an open trade in the same direction exists, or orderType=None, no action is taken"""
        if orderType == None or self.positionSize == 0: return
        if not self.hasOpenPosition() and self.checkMargin():
            activeAsset = self.market.getAsset(self.activeAssetId)
            self.positions.append(TradePosition(activeAsset,orderType,self.positionSize,activeAsset.getClosePrice(),entryBarNum=self.market.currentBarNum,enableCommission=self.enableCommission))
        elif self.getCurrentPosition().orderType != orderType:
            if allowExit: self.exitPosition()

    def exitPosition(self):
        """ exits current position, if any"""
        curPos = self.getCurrentPosition()
        if(curPos==None): return False
        curPos.closePosition()
        self.adjustBalance(curPos.getPositionValue())

    def adjustPositionSize(self,amount, verifyMarginReq=True, minPositionSize = 0):
        """ modifies current position size by given amount; if verifyMarginReq, then any adjustment which exceed margin reqs will be ignored; new position size will not exceed minPositionSize """
        newSize=self.positionSize+amount
        if newSize < minPositionSize: newSize = minPositionSize
        if verifyMarginReq and (self.getAccountValue() < (newSize * self.marginRequirement)): return
        self.positionSize=newSize

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
        self.accountLog.loc[curBar,'accountValue'] = self.getAccountValue(includeUnrealizedPL=True)
        self.accountLog.loc[curBar,'allTimePL'] = self.getRealizedPL()
        self.accountLog.loc[curBar,'unrealizedPL'] = self.getUnrealizedPL()
        self.accountLog.loc[curBar,'nTrades'] = len(self.positions)
        self.accountLog.loc[curBar,'positionStatus'] = self.getPositionStatus()
        self.accountLog.loc[curBar,'marginFlag'] = self.marginFlag

    def reset(self):
        """ reinits self """
        self.__init__(marketObj=self.market,initialBalance=self.initialBalance,marginRequirement=self.marginRequirement,enableCommission=self.enableCommission,positionSize=self.initPositionSize)





''' #Unused methods
def getUnrealizedPL(self): #save this for multiTrade capability - while copying to 120119, sticking with single trade approach for time (and training speed)
    """ returns net value of open positions """
    unrealizedPl = 0
    for i in self.positions:
        if i.isActive(): unrealizedPl+=i.getPositionValue()
    return unrealizedPl

'''