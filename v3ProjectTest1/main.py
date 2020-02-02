"""
120819
Main.py

main for v3
"""

import os
from datetime import timedelta

import RLTrade
from RLTrade import Assets, Market, TradingAccount
from RLTrade.assetTestData import assetDataLib
from RLTrade.agents.DQNAgent import DQNAgent
from RLTrade.experiments.RLTradingExperiment import RLTradingExperiment
#from ProjectEnvironments.testTradingEnv_basic import TestTradeEnv #import my custom environment
#from ProjectEnvironments.Env_basic_wPosSize import TestTradeEnv_PosSize #import my custom environment
from ProjectEnvironments.Env_componentTest import Env_011920 as CurrentEnvClass
from ProjectComponents import stateSets,actionSets,rewardSets

###############
# Data Prep
###############

assetData = assetDataLib.baseLineData2(tickDataSize=560) #560=100 bars |  #2560 = 500 bars
print('# of BARS: {}'.format(len(assetData)))

####################
# Component Setup
####################

stateSet = stateSets.stateSet1
actionSet = actionSets.longOnly_variablePositionSize
rewardSet = rewardSets.rewardSet1

####################
# Environment Setup
####################

#tradeReportPlot = RLTradeReportPlotter.RLTradeReportPlotter()

testAsset = Assets.FXAsset(assetData)
market = Market.Market([testAsset])

tradingAccount = TradingAccount.TradingAccount(market,initialBalance=500)

reportLogDir = os.path.dirname(os.path.abspath(__file__)) + '/reportLogs'
env = CurrentEnvClass(stateSet=stateSet,actionSet=actionSet,rewardSet=rewardSet,tradingAccount=tradingAccount,reportLogDir=reportLogDir,positionSizeAdjustmentIncrements=500)
state_size = env.getObservationSpaceSize()
action_size = env.getActionSpaceSize()

agent = DQNAgent(state_size, action_size)
#agent.load(reportLogDir+'/David_Storlie/Rosa_Blakely/Rosa_Blakely_ModelWeights.h5')

batch_size = 3 #for replay
nBarsPerReplay = 1 # this is how many bars between each agent replay call. The lower the number, the more often it's called (slower)

nEpisodes = 2

####################
# Experiment Setup
####################

# setup experiment callbacks

def onDone(experiment):
    d = env.getInfo()
    d['totalReward'] = env.report.iloc[-1]['totalReward']
    experiment.consoleMsg(d)
    
def onPostStep(experiment):
    #log agent predicted action values for next_state
    predictedActionValues = agent.query(experiment.state)[0]
    preActionDict = {'predValueAction_' + str(i): predictedActionValues[i] for i in range(len(predictedActionValues))}
    env.addReportData(preActionDict,market.currentBarNum-1)
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
        agent.__init__(state_size,action_size)
        agent.load('{}/{}_ModelWeights.h5'.format(env.getReportLogDir(),env.environmentID))
        market.assets[0].data = assetDataLib.baseLineData2(tickDataSize=560) #new asset test data
        env.reset(fullInit=True)
        env.environmentID = '{}_{}'.format(envId,i)
    expm = RLTradingExperiment(agent=agent,environment=env,callbacksDict=callbacksDict,nEpisodes=nEpisodes,cudaDevices="0")
    expm.consoleMsg('Starting Experiment {}/{}'.format(i,nExperiments))
    expm.run()

expm.consoleMsg("All experiments Complete.")
#==========
