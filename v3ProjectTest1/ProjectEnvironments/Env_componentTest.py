"""
122219
Env_componentTest.py

Testing the component system for state/action/rewards
"""

from RLTrade.environments import TradingEnvironment
#from RLTrade.rewardsLib import rewardsBrainstorm1 as rewards
from RLTrade.rewardsLib import rewardComponents as rewards
from RLTrade.rewardsLib import compoundRewards1 as rewards2
from RLTrade.observationsLib import stateComponents as stateFeatures
from RLTrade.actionsLib import actionComponents as actions

class Env_122219(TradingEnvironment.TradingEnvironment):
    def __init__(self,rewards,actions,stateFeatures,positionSizeAdjustmentIncrements=1000, **kwds):
        super().__init__(**kwds)

        self.posSizeIncrements = positionSizeAdjustmentIncrements

    def doAction(self, action):
        """ performs action on the environment """
        actions.doAction()