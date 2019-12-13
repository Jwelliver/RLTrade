"""
    120119 - Market Class
    Acts as a container for Assets and allows simulated bar-to-bar time flow by iterating the 'currentBarNum'
"""

class Market():
    def __init__(self, assetList):
        self.assets = assetList
        self.currentBarNum = 0

    def advance(self):
        """ advances currentBarNum """
        self.setCurrentBarNum(self.currentBarNum+1)
    
    def setCurrentBarNum(self, newBarNum):
        """ sets currentBarNum to newBarNum """
        self.currentBarNum = newBarNum
        for i in self.assets:
            i.currentBarNum = self.currentBarNum

    def getData(self, assetId, key=None, barNum='current', notFoundReturns=None):
        """ returns key at barNum from assetId; barNum=='current': currentBarNum will be used; barNum==None: All bars returned; if key==None, whole row is returned """
        return self.getAsset(assetId).getData(key,barNum,notFoundReturns)

    def getOHLC(self,assetId, barNum='current'):
        """ Returns OHLC Dataframe at given barNum; barNum=='current': currentBarNum; barNum==None: all bars """
        return self.getAsset(assetId).getOHLC(barNum)

    def getBarCount(self):
        """ returns nBars in asset[0] """ #todo: will need to make this useful for multiple assets. Maybe require that all assets in a market contain same number of datapoints/bars
        return self.getAsset(0).getBarCount()

    def getAsset(self, assetId):
        """ returns asset object from assetId """
        return self.assets[assetId]
    
    def reset(self):
        """ resets market back to bar 0 """
        self.setCurrentBarNum(0)