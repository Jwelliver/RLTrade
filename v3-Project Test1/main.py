"""
120819
Main.py

main for v3
"""
import os

import RLTrade
from RLTrade import Assets, Market, TradingAccount
from RLTrade.assetTestData import assetDataLib
from RLTrade.agents.DQNAgent import DQNAgent
from RLTrade.experiments.RLTradingExperiment import RLTradingExperiment
from testTradingEnv import TestTradeEnv #import my custom environment, tailored to this experiment

###############
 # Data Prep
###############

assetData = assetDataLib.baseLineOHLCData2()

####################
 # Environment Setup
####################

#tradeReportPlot = RLTradeReportPlotter.RLTradeReportPlotter()

testAsset = Assets.FXAsset(assetData)

market = Market.Market([testAsset])
tradingAccount = TradingAccount.TradingAccount(market,initialBalance=100)

reportLogDir = os.path.dirname(os.path.abspath(__file__)) + '/reportLogs'
env = TestTradeEnv(tradingAccount=tradingAccount,reportLogDir=reportLogDir)
state_size = env.getObservationSpaceSize()
action_size = env.getActionSpaceSize()

agent = DQNAgent(state_size, action_size)

batch_size = 32 #for replay
nBarsPerReplay = 1 # this is how many bars between each agent replay call. The lower the number, the more often it's called (slower)

nEpisodes = 10

####################
 # Experiment Setup
####################

# setup custom experiment methods

def onDone(experiment):
    print(env.getInfo())

def onPostStep(experiment):
    #handle DQN memory
    experiment.agent.remember(experiment.state, experiment.action, experiment.reward, experiment.next_state, experiment.done)
    #handle DQN replays
    if experiment.barNum % nBarsPerReplay == 0 and len(experiment.agent.memory) > batch_size:
        experiment.agent.replay(batch_size)

callbacksDict = {'onPostStep': onPostStep, 'onDone': onDone }

# init and run experiment

expm = RLTradingExperiment(agent=agent,environment=env,callbacksDict=callbacksDict,nEpisodes=nEpisodes)
expm.run()
