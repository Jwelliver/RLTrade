"""
120819
RLTradingExperiment class

"""

import os

from .RLExperiment import RLExperiment

class RLTradingExperiment(RLExperiment):
    def __init__(self,**kwds):
        super().__init__(**kwds) #todo check
        self.barNum = 0

    def runEpisode(self):
        """ iterates through all bars """
        nBars = self.env.market.getBarCount()
        self.barNum = 0 #reset
        for self.barNum in range(nBars):
            self.mainUpdate()
            if self.done: break