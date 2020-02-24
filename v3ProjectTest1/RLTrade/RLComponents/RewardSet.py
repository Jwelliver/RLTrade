"""
122819
RewardSet.py

"""

from RLTrade.RLComponents.RLComponentSet import RLComponentSet

class RewardSet(RLComponentSet):

    def __init__(self,defaultRewardValue=None,**kwds):
        """ RewardComponent index corresponds to Environment's eventflag for when they'll be called. i.e. reward method at index 2 will be called when the environment's event flag is 2; defaultRewardValue will be used for eventflags with no corresponding reward function. if defaultRewardValue==None, then Reward @ Index 0 is used."""
        super().__init__(**kwds)
        self.defaultRewardValue = defaultRewardValue

    def getReward(self):
        """ returns sum of reward functions """
        totalReward = 0
        curEventFlag = self.env.eventFlag
        for i in self.componentList:
            if i.metadata['eventFlag_exclude'] != None:
                if curEventFlag in i.metadata['eventFlag_exclude']: continue
            if i.metadata['eventFlag'] == None or curEventFlag in i.metadata['eventFlag']:
                    totalReward += i.call()
        return totalReward

    def add(self,callback,id=None,description=None,eventFlagInclude=None,eventFlagExclude=None,kwargRef=None,metadata=None):
        """ creates Reward Component from a given function; Use eventFlagInclude/exclude to specify which event flags this component function should run on. If None, they will ignore eventFlags and always be called."""
        if metadata==None: metadata = {}
        if kwargRef==None: kwargRef = {}
        kwargRef['env'] = self.env #ensure env reference is included
        if eventFlagInclude!=None: 
            if not type(eventFlagInclude) is list: eventFlagInclude = list(eventFlagInclude)
        if eventFlagExclude!=None: 
            if not type(eventFlagExclude) is list: eventFlagExclude = list(eventFlagExclude)
        metadata['eventFlag'] = eventFlagInclude
        metadata['eventFlag_exclude'] = eventFlagExclude
        super().add(callback,id,description=description,kwargRef=kwargRef,metadata=metadata)