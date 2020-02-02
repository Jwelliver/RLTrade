"""
122819
ActionSet.py

Subclass of RLComponentSet to contain actions
"""

from RLTrade.RLComponents.RLComponentSet import RLComponentSet

class ActionSet(RLComponentSet):

    def __init__(self,**kwds):
        super().__init__(**kwds)

    def doAction(self,actionInt):
        """ does given action """
        self.componentList[actionInt].call()
