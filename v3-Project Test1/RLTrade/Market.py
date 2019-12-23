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

    def getOHLC(self, assetId, barNum='current'):
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

    def getAssetDataFeatures(self,assetIdList,featureKeyList):
        """ returns requested feature values from each asset in assetIdList """
        assetIdList = self.getAssetIdListFromValue(assetIdList)
        features = []
        for i in assetIdList:
            for k in featureKeyList:
                features.append(self.getData(i,k))
        return features

    def getAssetIdListFromValue(self, valueToCheck, excludeInvalids=True):
        """ takes a value or list of values (can be existing assetId (as int) or asset name (as str)) and returns a list of verified assetId if found. If not found, returns None """
        if not isinstance(valueToCheck,list): valueToCheck = [valueToCheck]
        verifiedIdList = []
        if len(self.assets) == 0: return []
        for i in valueToCheck:
            id = None
            if type(i) is int: 
                if i >= 0 and i <= len(self.assets)-1: id = i
            elif type(i) is str:
                id = self.getAssetIdByName(i)
            if id == None and excludeInvalids: continue
            verifiedIdList.append(id)
        return verifiedIdList

    def getAssetIdByName(self, assetName):
        """ returns assetId by assetName; returns None if not found. """
        for i in range(len(self.assets)):
            if self.assets[i].name==assetName: return i
        return None