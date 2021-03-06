"""
122819
RLEnvironment

Superclass for Environments in this framework

"""

import gym
import numpy as np
import pandas as pd
import copy
import datetime
import os
import names

class RLEnvironment(gym.Env):

    def __init__(self, stateFeatureFunctions, actionFunctions, rewardFunctions, reportLogDir="./reportLogs"):

        self.stateFeautures = stateFeatureFunctions
        self.actions = actionFunctions
        self.rewards = rewardFunctions

        self.reportHistory = []
        self.report = pd.DataFrame() #collects data for export/analysis
        self.reportLogDir = reportLogDir
        self.environmentID = self.generateEnvironmentId() #random string used as a unique ID when exporting a group of sim reports
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

    def reset(self,fullInit=False):
        """Resets the state of the environment and returns an initial observation.
        Returns:
            observation (object): the initial observation.
        """
        self.simNum+=1
        self.reinitialize(fullInit)
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
        self.setEventFlag()
        self.setStopFlag()

    def getActionSpace(self):
        """ returns action space obj """
        return gym.spaces.Discrete(len(self.actions.componentList))
    
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

    def reinitialize(self,fullInit=False):
        """ re-initializes environment for new start  - adds current sim to sim history, uses it's ohlc and starting balance to reinit new tradingSim """
        if fullInit: self.__init__(tradingAccount=self.trader,reportLogDir=self.reportLogDir)
        self.reportHistory.append(self.report)
        self.report = pd.DataFrame() # reset report
        self.eventFlag = 0
        self.stopFlag = 0

    def setEventFlag(self):
        """ sets a unique integer which is used to represent the occurence of certain conditions in the environment. The flag can be used to determine which reward is given. """
       pass

    def setStopFlag(self):
        """ sets the stop flag based on certain conditions """
        self.stopFlag = self.eventFlag #default  uses the event flags to determine if a stop condition has been met

    def isDone(self):
        """ returns current isDone value as a bool """
        return self.stopFlag != 0
    
    def getInfo(self):
        """ returns info from current state as a dict """
        infoDict = {}
        return infoDict
    
        ####################### #TODO: this might belong better in RLExperiment
        # DATA EXPORT METHODS
        #######################

    def generateEnvironmentId(self):
        """ returns unique name used for exporting the group of data """
        n = names.get_full_name().replace(' ','_')
        dirPath = self.getReportLogDir(mainDirOnly=True) + '/' + n
        while os.path.exists(dirPath) == True:
            n = self.generateEnvironmentId()
        return n

    def getReportLogDir(self, mainDirOnly = False):
        """ returns path of dir log with a subfolder using the environmentId; mainDirOnly=True will only return the mainDir path without the subfolder"""
        return self.reportLogDir if mainDirOnly else self.reportLogDir + "/" + self.environmentID

    def logReportData(self,observation,reward,done,info):
        """ logs reportData """
        logData = {}
        barNum = self.market.currentBarNum
        activeAssetId = self.trader.activeAssetId
        logData.update(self.market.getOHLC(activeAssetId).to_dict())
        logData.update({'stateFeature_' + str(i): observation[i] for i in range(len(observation))})
        logData['reward'] = reward
        if barNum == 0: logData['totalReward'] = reward
        else: logData['totalReward'] = self.report.iloc[-1]['totalReward'] +reward
        logData.update(info)
        logData['positionStatus'] = self.trader.getPositionStatus()
        logData['positionSize'] = self.trader.positionSize
        tradeJustOpened = self.trader.getPositionOpenedOnLastBar()
        tradeJustClosed = self.trader.getPositionClosedOnLastBar()
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
        if os.path.exists(dirPath) == False: os.makedirs(dirPath)
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
        tradeAction = self.getActionDict()[action]
        self.trader.enterPosition(tradeAction)

    def getStateObservation(self):
        """ returns current observation """
        return stateFeatures.getStateObservation()

    def getReward(self):
        """ returns current reward as a float accounting for the current eventFlag; returns 0 if reward does not exist for the existing eventFlag """ #122119: commenting out try/except for now
        return rewards.getReward()