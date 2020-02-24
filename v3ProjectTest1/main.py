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
from ProjectEnvironments.Env_componentTest import Env_011920 as CurrentEnvClass
from ProjectComponents import stateSets,actionSets,rewardSets

###############
#  Var Prep
###############

marketStartBarNum = 50 
batch_size = 10 #for replay
nBarsPerReplay = 5 # this is how many bars between each agent replay call. The lower the number, the more often it's called (slower)
nEpisodes = 15
nExperiments = 2


###############
# Data Prep
###############

assetData = assetDataLib.baseLineData0(tickDataSize=1750,ohlc_colNames=['o','h','l','c']) #500=100 bars |  #2560 = 500 bars
print('# of BARS: {}'.format(len(assetData)))

####################
# Component Setup
####################

stateSet = stateSets.stateSet3_taWindowTest
actionSet = actionSets.longShort
rewardSet = rewardSets.pctChangeInAccValOnClose

####################
# Environment Setup
####################

#tradeReportPlot = RLTradeReportPlotter.RLTradeReportPlotter()

testAsset = Assets.FXAsset(assetData)
market = Market.Market([testAsset])

tradingAccount = TradingAccount.TradingAccount(market,initialBalance=500)

reportLogDir = os.path.dirname(os.path.abspath(__file__)) + '/reportLogs'
env = CurrentEnvClass(stateSet=stateSet,actionSet=actionSet,rewardSet=rewardSet,tradingAccount=tradingAccount,marketStartBarNum=marketStartBarNum,reportLogDir=reportLogDir,positionSizeAdjustmentIncrements=500)
state_size = env.getObservationSpaceSize()
action_size = env.getActionSpaceSize()

agent = DQNAgent(state_size, action_size)
#agent.load(reportLogDir+'/David_Storlie/Rosa_Blakely/Rosa_Blakely_ModelWeights.h5')

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
    preActionDict.update({'epsilon': agent.epsilon})
    env.addReportData(preActionDict,market.currentBarNum-1)
    #handle DQN memory
    experiment.agent.remember(experiment.state, experiment.action, experiment.reward, experiment.next_state, experiment.done)
    #handle DQN replays
    if experiment.barNum % nBarsPerReplay == 0 and len(experiment.agent.memory) > batch_size:
        experiment.agent.replay_orig(batch_size)

def onExperimentReset(experiment):
    #create new test data
    experiment.environment.market.assets[0].data = assetDataLib.baseLineData0(tickDataSize=500) #new asset test data

callbacksDict = {'onPostStep': onPostStep, 'onDone': onDone, 'onExperimentReset': onExperimentReset }

##########################
# Experiment Init and Run
##########################

expm = RLTradingExperiment(agent=agent,environment=env,callbacksDict=callbacksDict,nEpisodes=nEpisodes,cudaDevices="0")
expm.runMultiple(nExperiments=nExperiments,reuseAgent=True, reinitAgent=True)

#==========
