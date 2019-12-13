"""
120819
Main.py

main for v3
"""


from RLTrade import * #immport RLTrade framework
from testTradingEnv import TestTradeEnv #import my custom environment, tailored to this experiment

###############
 # Data Prep
###############

assetData = assetDataLib.baseLineData1()

####################
 # Environment Setup
####################

#tradeReportPlot = RLTradeReportPlotter.RLTradeReportPlotter()

testAsset = Assets.FXAsset(assetData)

market = Market.Market([testAsset])
tradingAccount = TradingAccount.TradingAccount(market,initialBalance=10000)

env = TestTradeEnv(tradingAccount)
state_size = env.getObservationSpaceSize()
action_size = env.getActionSpaceSize()

agent = DQNAgent(state_size, action_size)

batch_size = 32 #for replay
nBarsPerReplay = 5 # this is how many bars between each agent replay call. The lower the number, the more often it's called (slower)

####################
 # Experiment Setup
####################

# setup custom experiment methods

def onDone(experiment):
    if experiment.barNum % nBarsPerReplay == 0 and len(experiment.agent.memory) > batch_size:
    #print("Running Replay | bar: {}".format(barNum))
    #print("barNum%nBarsPerReplay: {}".format(barNum % nBarsPerReplay))
    #print(str(time.time() - startTime))
    experiment.agent.replay(batch_size)

def onStep(experiment):
    experiment.agent.remember(experiment.state, experiment.action, experiment.reward, experiment.next_state, experiment.done)

userMethods = {'onDone': onDone, 'onStep': onStep}

# init and run experiment

expm = experiments.RLTradingExperiment(agent=agent,environment=env,userMethodsDict=userMethods)
expm.run()
