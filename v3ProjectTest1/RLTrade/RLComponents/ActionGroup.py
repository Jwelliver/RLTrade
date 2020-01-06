"""
122819
ActionGroup.py

Subclass of RLComponentGroup to contain actions
"""

from RLTrade.RLComponents import RLComponentGroup

class ActionGroup(RLComponentGroup):

    def __init__(self,**kwds):
        super().__init__(**kwds)

    def doAction(actionInt):
        """ does given action """
        self.componentList[actionInt].call()
