"""
120819
TradeEnv

Framework environment for use with a TraderAccount and Market.
This can be subclassed to set up individual experiments.


"""

import gym
from rewardsLib import rewardsBrainstorm1 as rewardsLib
from observationsLib import observationsBrainstorm1 as observationsLib
import numpy as np
import pandas as pd
import copy
import datetime
import os
import names

class TradingEnv(gym.Env):

    def __init__(self, traderController):
        self.trader = rlTradeController
        self.market = rlTradeController.market

        self.action_space = self.getActionSpace()
        self.observation_space = self.getObservationSpace()

        self.environmentID = self.generateEnvironmentId() #random string used as a unique ID when exporting a group of sim reports
        self.reportHistory = []
        self.report = pd.DataFrame() #collects data for export/analysis
        
        self.simNum = 0 #tracks resets to log simNum data
        self.eventFlag = 0 # updated each update(); Rewards can differ based on this.
        self.stopFlag = 0 # setting this to anything other than 0 will trigger the default isDone() bool.

        #reward_range = () # set this if you want to limit min/max reward, otherwise, it's automatically inifinte


    def step(self, action):
        """Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.
        Accepts an action and returns a tuple (observation, reward, done, info).
        Args:
            action (object): an action provided by the agent
        Returns:
            observation (object): agent's observation of the current environment
            reward (float) : amount of reward returned after previous action
            done (bool): whether the episode has ended, in which case further step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning)
        """
        self.doAction(action)
        self.updateEnv()
        observation = self.getStateObservation()
        reward = self.getReward()
        done = self.isDone()
        info = self.getInfo()
        self.logReportData(observation,reward,done,info)
        self.addReportData({'action': action}, self.market.currentBarNum-1) #log last bar's action
        return observation,reward,done,info

    def reset(self):
        """Resets the state of the environment and returns an initial observation.
        Returns:
            observation (object): the initial observation.
        """
        self.simNum+=1
        self.reinitialize()
        initialObservation = self.getStateObservation()
        self.logReportData(initialObservation,0,self.isDone(),self.getInfo())
        return initialObservation

    def render(self, mode='human'):
        self.textRender()
        #raise NotImplementedError

    def seed(self, seed=None):
        return

    ##########################################################
    # Below are custom methods ie., non-gym

    def updateEnv(self):
        """ called on step, handles step updates """
        self.market.advance()
        self.setEventFlag()
        self.setStopFlag()

    def getActionSpace(self):
        """ returns action space obj """
        actDict = self.getActionDict()
        return gym.spaces.Discrete(len(actDict))
    
    def getActionSpaceSize(self):
        """ returns size of action space """
        return self.getActionSpace().n

    def getObservationSpace(self):
        """ returns observation space obj - size will be used by agent to determine network input size"""
        nFeatures = len(self.getStateObservation())
        return gym.spaces.Box(low=-np.inf,high=np.inf,shape=(nFeatures,) )

    def getObservationSpaceSize(self):
        """ returns size of observation space """
        return self.getObservationSpace().shape[0]

    def reinitialize(self):
        """ re-initializes environment for new start  - adds current sim to sim history, uses it's ohlc and starting balance to reinit new tradingSim """
        self.reportHistory.append(self.report)
        self.report = pd.DataFrame() # reset report
        self.market.reset()
        self.trader.reset()

    def getReward(self):
        """ returns current reward as a float accounting for the current eventFlag """
        #Note: Do not override this - Override getRewardDict() instead.
        return self.getRewardDict()[self.eventFlag]

    def setEventFlag(self):
        """ sets a unique integer which is used to represent the occurence of certain conditions in the environment. The flag is used to determine which reward is given. e.g. if the account has a margin call after the last step, the flag is set, making the margin call visible to the reward function.
        returns:
            0: normal; no even.
            1: reached end of ohlc data
            2: marginCall
            3: financial ruin / not enough margin to place another trade
        """
        if self.market.currentBarNum >= len(self.market.assets[0].data)-1:
            self.eventFlag = 1
        if self.tradingAccount.checkMargin() == False:
            self.eventFlag =  self.tradingAccount.marginFlag
        self.eventFlag = 0

    def setStopFlag(self):
        """ sets the stop flag based on certain conditions """
        self.stopFlag = self.eventFlag #default  uses the event flags to determine if a stop condition has been met

    def isDone(self):
        """ returns current isDone value as a bool """
        return self.stopFlag != 0
    
    def getInfo(self):
        """ returns info from current state as a dict """
        simNum = self.simNum
        barNum = self.market.currentBarNum
        nTrades = len(self.rlTradeController.tradingAccount.positions)
        isTradeOpen = self.rlTradeController.tradingAccount.hasOpenPosition()
        accVal = self.rlTradeController.tradingAccount.getAccountValue(includeUnrealizedPL=True)
        #lastBarVal = accVal
        #if len(self.rlTradeController.tradingAccount.accountValueHistory) > 2:
        #    lastBarVal = self.rlTradeController.tradingAccount.accountValueHistory[-2]
        #accChangeSinceLastBar = accVal - lastBarVal
        accChangeSinceSimStart = accVal - self.rlTradeController.tradingAccount.initialBalance
        stopConditions = self.rlTradeController.getStopConditions()
        infoDict = {'simNum': simNum, 'barNum': barNum, 'nTrades':nTrades, 'tradeOpen':isTradeOpen, 'accountValue': accVal, 'allPL':accChangeSinceSimStart, 'stopConditions': stopConditions}
        return infoDict
    
        ####################### #TODO: this should probably
        # DATA EXPORT METHODS
        #######################

    def generateEnvironmentId(self):
        """ returns unique name used for exporting the group of data """
        n = names.get_full_name().replace(' ','_')
        dirPath = self.getReportLogDir(mainDirOnly=True) + '/' + n
        while os.path.exists(dirPath) == True:
            n = names.get_full_name().replace(' ','_')
        return n

    def getReportLogDir(self, mainDirOnly = False):
        """ returns path of dir log; mainDirOnly=False will inlcude the sub folder using the environmentID """
        mainDir = './reportLogs'
        return mainDir if mainDirOnly else mainDir + "/" + self.environmentID

    def logReportData(self,observation,reward,done,info):
        """ logs reportData at the currentBar """
        #barNum,ohlc,stateFeatures,currentAccVal,deltaPL_lastBar,deltaPL_start,nTrades,entryPrice,exitPrice,positionStatus
        logData = {}
        barNum = self.market.currentBarNum
        activeAssetId = self.rlTradeController.tradingAccount.activeAssetId
        logData.update(self.market.getOHLC(activeAssetId).to_dict())
        logData.update({'stateFeature_' + str(i): observation[i] for i in range(len(observation))})
        logData['reward'] = reward
        logData.update(info)
        logData['positionStatus'] = self.rlTradeController.tradingAccount.getPositionStatus()
        tradeJustOpened = self.rlTradeController.tradingAccount.getPositionOpenedOnLastBar()
        tradeJustClosed = self.rlTradeController.tradingAccount.getPositionClosedOnLastBar()
        logData['entryPrice'] = "" if tradeJustOpened==None else tradeJustOpened.entryPrice
        logData['exitPrice'] = "" if tradeJustClosed==None else tradeJustClosed.exitPrice
        self.addReportData(logData,barNum)
    
    def addReportData(self,dictData,barNum):
        """ adds the contents of the dict to the report dict at the given barNum """
        for k,v in dictData.items():
            self.report.loc[barNum, k] = v
        #self.report.iloc[barNum] = dictData

    def exportReportToCsv(self):
        """ exports report data about the given sim to csv """
        #nowStr = datetime.datetime.now().strftime('%Y-%m-%d %H.%M')
        dirPath = self.getReportLogDir() 
        if os.path.exists(dirPath) == False:
            os.makedirs(dirPath) ,
        fullPath = dirPath + '/' + self.environmentID + "_" + str(self.simNum) +'.csv'
        self.report.to_csv(fullPath,mode='w+')

        #############################
        # PRIMARY METHODS TO OVERRIDE
        #############################
    
    def getActionDict(self):
        """ returns dictionary where keys are indexes and values are arbitrary action values which will be used by the doAction() method """
        return { 0: None, 1: 'buy', 2: 'sell'}

    def doAction(self, action):
        """ performs action on the environment """
        #Default: 0 = do nothing; 1 = Buy; 2 = Sell
        tradeAction = getActionDict()[action]
        self.trader.enterPosition(tradeAction)

    def getStateObservation(self):
        """ returns current observation """
        pass

    def getRewardDict(self):
        """ returns the current reward for each eventFlag - You can set eventFlags in self.getEventFlag() """
        normalReward = 1
        rewardDict = {
            0: normalReward,
            1: normalReward,
            2: -10,
            3: -10,
        }
        return rewardDict