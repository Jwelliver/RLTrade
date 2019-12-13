"""
    120119

    
"""


class TradePosition():

    def __init__(self, asset, orderType, positionSize, entryPrice, entryBarNum, entryTime=None, exitPrice=None, exitTime = None, exitBarNum=None,enableCommission=True):
        """ inits - orderType must be 'buy' or 'sell' """
        self.asset = asset
        self.orderType = str(orderType).lower()
        self.positionSize = positionSize
        self.entryPrice = entryPrice
        self.entryTime = entryTime
        self.entryBarNum = entryBarNum
        self.exitPrice = exitPrice
        self.exitTime = exitTime
        self.exitBarNum = exitBarNum
        self.enableCommission = enableCommission

    def closePosition(self):
        """ updates the exitPrice and closes the trade """
        self.exitPrice = self.asset.getClosePrice()
        self.exitBarNum = self.asset.currentBarNum
        #self.exitTime = exitTime
        
    def isActive(self):
        """ returns true if trade is open. i.e. if exitPrice == None """
        return (self.exitPrice == None)
    
    def getOrderTypeInt(self):
        """ returns 1 for buy or -1 for sell; silly temp function to handle conversion to an int """
        return 1 if self.orderType=="buy" else -1

    def getNetPips(self, price=None):
        """ returns net pips from the given price to currentPrice, or to the exitPrice if trade is closed; pips are positive if in dir of trade """
        if price==None:
            price = self.exitPrice if not self.isActive() else self.asset.getClosePrice()
        return ((price - self.entryPrice) * self.asset.pipMultiplier) * self.getOrderTypeInt()
    
    def getPositionValue(self,price=None,useNetValue=True):
        """ returns position value in dollars from given price; if price==None and trade is closed, exit price is used; if trade is not closed then 0 is returned; if useNetValue, then total(roundtrip) commission will be factored into the value"""
        netModifier = self.getCommissionValue() if useNetValue else 0
        return ((self.getNetPips(price) * self.positionSize) /10000) + netModifier
    
    def getCommissionValue(self):
        """ returns commission value in dollars or 0 if disabled """
        return -(self.positionSize/10000) if self.enableCommission else 0
