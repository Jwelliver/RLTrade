"""
120819
RLTradingExperiment class

"""

import os
from RLExperiment import RLExperiment

class RLTradingExperiment(RLExperiment):
    def __init__(self):
        super.__init__() #todo check

    def run(self):
        """ starts training over nEpisodes """
        nBars = self.env.market.getBarCount()
        self.onExperimentStart()
        for e in range(nEpisodes):
            for barNum in range(nBars):
                self.onNewEpisode(resetEnv=True)
                self.mainUpdate()
                if self.done:
                    self.onDone()
                    break