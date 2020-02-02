"""
011920
Env_componentTest.py

Testing the component system for state/action/rewards
"""

from RLTrade.environments import TradingEnvironment

class Env_011920(TradingEnvironment.TradingEnvironment):
    def __init__(self,positionSizeAdjustmentIncrements=1000, **kwds):
        super().__init__(**kwds)

        self.posSizeIncrements = positionSizeAdjustmentIncrements

    '''
    def doAction(self, action):
        """ performs action on the environment """
        self.actionSet.doAction()
    '''