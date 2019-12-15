"""
    120119 - Asset Class
    Container for OHLC data and other by-bar meta data
"""

class Asset():
    def __init__(self, assetDataframe, name='', type='Generic'): # 120119 currently expecting the index to be integers representing barNums
        self.data = assetDataframe
        self.type = type
        self.name = name
        self.currentBarNum = 0
    
    def getData(self,key=None,barNum='current',notFoundReturns=None):
        """ returns value of given key at given barNum; barNum=='current': currentBarNum will be used; barNum==None: All bars returned; if key==None, whole row is returned """
        if barNum=='current': barNum = self.currentBarNum
        try:
            return self.data.iloc[barNum] if key==None else self.data.iloc[barNum][key]
        except:
            return notFoundReturns
    
    def getOHLC(self,barNum='current'):
        """ Returns OHLC Dataframe at given barNum; barNum=='current': currentBarNum; barNum==None: all bars """
        if barNum=='current': barNum = self.currentBarNum
        return self.data.iloc[barNum][['o','h','l','c']] if barNum!=None else self.data[['o','h','l','c']]

    def getClosePrice(self,barNum='current'):
        """ returns close price at given barNum; barNum=='current': currentBarNum; barNum==None: all bars """
        return self.getData('c',barNum) if barNum != None else self.data['c']

    def getBarCount(self):
        """ returns number of close prices in data """
        return len(self.data['c']) -1
        

"""
    FXAsset 
    Has properties unique to FX
"""

class FXAsset(Asset):
    def __init__(self,assetDataframe, name='FXPair1', pipMultiplier=10000):
        super().__init__(assetDataframe,name,type='FX')
        self.pipMultiplier = pipMultiplier