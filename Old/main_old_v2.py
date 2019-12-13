"""
120119
Main Experiment Training file.

"""


import keras


'''
    the model is going to be approximating the next state's reward for each action given a state as input.
        input size = state space size
        output size = action space size

    for each episode, 
        -update the env (reset at beginning, then step until done with epoch)
        -get action to take (use getAction(state) func.. implement exploration, and random choice if options are identical)
        -take the chosen action in the env, obtain the new state and rewards
        -update model using fit with previous state as input, and the actual reward for the action taken as a target. all other rewards should remain unchanged


'''

import os
import random
import gym
import numpy as np
import pandas as pd
from collections import deque
from DQNAgent import DQNAgent
from matplotlib import pyplot as plt
from sklearn import preprocessing
from datetime import timedelta
import time

import TradeEnv
import Market
import Assets
import TradingAccount
import RLTradeController

import assetDataLib
import testDataGeneration as testDataGen
#import RLTradeReportPlotter
#import TradePosition,TradingSim,TradeEnv1


#################
 # GPU Selection
#################

os.environ["CUDA_VISIBLE_DEVICES"]="0" #  '-1' = CPU,  '0,1' makes both GPUs visible.

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
account = TradingAccount.TradingAccount(market,initialBalance=10000)
rlTradeController = RLTradeController.RLTradeController(account,market)

env = TradeEnv.TradingEnv(rlTradeController)
state_size = env.getObservationSpace().shape[0]
action_size = env.action_space.n

agent = DQNAgent(state_size, action_size)

nEpisodes = 2
batch_size = 32 #for replay
nBarsPerReplay = 5 # this is how many bars between each agent replay call. The lower the number, the more often it's called (slower)

nBars = market.getBarCount()

####################
 # Experiment Run
####################

print("Begin")
totalTime = 0

done = False

for e in range(nEpisodes):
    print('===============================\n--------> Starting Episode {}/{}'.format(e+1,nEpisodes))
    startTime = time.time()
    state = env.reset()
    state = np.reshape(state, [1, state_size])
    for barNum in range(nBars):
        #print('e: {} | bar: {}/{}'.format(e,barNum,nBars))
        #env.render()
        action = agent.act(state)
        next_state, reward, done, info = env.step(action)
        #reward = reward if not done else -10
        next_state = np.reshape(next_state, [1, state_size])
        agent.remember(state, action, reward, next_state, done)
        state = next_state
        if done:
            finishTime = time.time() - startTime
            totalTime += finishTime
            nRemainingEpisodes = (nEpisodes - (e+1))
            timeRemaining = (totalTime/(e+1)) * nRemainingEpisodes
            print("Episode {} completed in {} seconds. | {} episodes ({}) remaining".format(e,timedelta(seconds=finishTime),nRemainingEpisodes,timedelta(seconds=timeRemaining)))
            print(info)
            #tradeReportPlot.plotTradeSimReport(env.getReportDataframe(),pauseOnShow=False)
            env.exportReportToCsv()
            #print("episode: {}/{}, score: {}, e: {:.2}".format(e, nEpisodes, time, agent.epsilon))
            break
        if barNum % nBarsPerReplay == 0 and len(agent.memory) > batch_size: #112419 see 11/24/19 progress notes 
            #print("Running Replay | bar: {}".format(barNum))
            #print("barNum%nBarsPerReplay: {}".format(barNum % nBarsPerReplay))
            #print(str(time.time() - startTime))
            agent.replay(batch_size)

print(" ======================== \n ----------> ALL episodes completed in {} | -- Saving Model -> {} \n========================".format(timedelta(seconds=totalTime),env.getReportLogDir()))
    agent.save(env.getReportLogDir()+"/"+env.environmentID + '_ModelWeights.h5')