"""
122819
StateFeatureGroup.py

"""

from RLTrade.RLComponents import RLComponentGroup

class StateFeatureGroup(RLComponentGroup):

    def __init__(self,excludeDisabledFeatures=True,**kwds):
        """ if excludeDisabledFeatures = false, all disabled features will be included in the observation, but with a default value """
        super().__init__(**kwds)
        self.excludeDisabledFeatures = excludeDisabledFeatures
        self.defaultValue = 0

    def getStateFeatures():
        """ returns stateFeatures """
        stateFeatures = []
        for i in self.componentList:
            featureValue = self.defaultValue
            if not i.enabled: if self.excludeDisabledFeatures: continue
            else: featureValue = i.call()
            stateFeatures.append(featureValue)
        return stateFeatures