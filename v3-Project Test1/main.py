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
from ProjectEnvironments.testTradingEnv_basic import TestTradeEnv #import my custom environment
from ProjectEnvironments.Env_basic_wPosSize import TestTradeEnv_PosSize #import my custom environment

from datetime import timedelta


###############
# Data Prep
###############

assetData = assetDataLib.baseLineData2(tickDataSize=2560) #560=100 bars |  #2560 = 500 bars
print('# of BARS: {}'.format(len(assetData)))

####################
# Environment Setup
####################

#tradeReportPlot = RLTradeReportPlotter.RLTradeReportPlotter()

testAsset = Assets.FXAsset(assetData)
market = Market.Market([testAsset])

tradingAccount = TradingAccount.TradingAccount(market,initialBalance=100)

reportLogDir = os.path.dirname(os.path.abspath(__file__)) + '/reportLogs'
env = TestTradeEnv_PosSize(tradingAccount=tradingAccount,reportLogDir=reportLogDir,positionSizeAdjustmentIncrements=500)
state_size = env.getObservationSpaceSize()
action_size = env.getActionSpaceSize()

agent = DQNAgent(state_size, action_size)
#agent.load(reportLogDir+'/David_Storlie/Rosa_Blakely/Rosa_Blakely_ModelWeights.h5')

batch_size = 5 #for replay
nBarsPerReplay = 5 # this is how many bars between each agent replay call. The lower the number, the more often it's called (slower)

nEpisodes = 1

####################
# Experiment Setup
####################

# setup custom experiment me-thods

def onDone(experiment):
    experiment.consoleMsg(env.report.iloc[-1])
    experiment.consoleMsg(env.getInfo())
    
def onPostStep(experiment):
    #handle DQN memory
    experiment.agent.remember(experiment.state, experiment.action, experiment.reward, experiment.next_state, experiment.done)
    #handle DQN replays
    if experiment.barNum % nBarsPerReplay == 0 and len(experiment.agent.memory) > batch_size:
        experiment.agent.replay_orig(batch_size)

callbacksDict = {'onPostStep': onPostStep, 'onDone': onDone }

# init and run experiment

nExperiments = 1

envId = env.environmentID
for i in range(nExperiments):

    if i>0: 
        agent.load('{}/{}_ModelWeights.h5'.format(env.getReportLogDir(),env.environmentID))
        #need to also reset/generate new test data
        env.reset(fullInit=True)
        env.environmentID = '{}_{}'.format(envId,i)
    expm = RLTradingExperiment(agent=agent,environment=env,callbacksDict=callbacksDict,nEpisodes=nEpisodes,cudaDevices="0")
    expm.run()

expm.consoleMsg("All experiments Complete.")
#==========
