"""
122819
RewardGroup.py

"""

from RLTrade.RLComponents import RLComponentGroup

class RewardGroup(RLComponentGroup):

    def __init__(self,defaultRewardValue=None,**kwds):
        """ RewardComponent index corresponds to Environment's eventflag for when they'll be called. i.e. reward method at index 2 will be called when the environment's event flag is 2; defaultRewardValue will be used for eventflags with no corresponding reward function. if defaultRewardValue==None, then Reward @ Index 0 is used."""
        super().__init__(**kwds)
        self.defaultRewardValue = defaultRewardValue

    def getReward():
        """ returns reward"""
        eventFlag = self.env.eventflag
        if eventFlag <= len(self.componentList) - 1: return self.componentList[self.env.eventflag].call()
        return self.defaultRewardValue if self.defaultRewardValue!=None else self.componentList[0].call()