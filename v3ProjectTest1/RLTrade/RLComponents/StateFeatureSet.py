"""
122819
StateFeatureSet.py

"""

from RLTrade.RLComponents.RLComponentSet import RLComponentSet

class StateFeatureSet(RLComponentSet):

    def __init__(self,excludeDisabledFeatures=True,**kwds):
        """ if excludeDisabledFeatures = false, all disabled features will be included in the observation, but with a default value """
        super().__init__(**kwds)
        self.excludeDisabledFeatures = excludeDisabledFeatures
        self.defaultValue = 0

    def getStateFeatures(self):
        """ returns stateFeatures """
        stateFeatures = []
        for i in self.componentList:
            featureValue = self.defaultValue
            if not i.enabled: 
                if self.excludeDisabledFeatures: continue
            else: featureValue = i.call()
            stateFeatures.append(featureValue)
        return stateFeatures