"""
120819
RLExperiment class

There's a lot of odd/discomforting global usage here, but it's the only way I saw fit to make it modular in my tired state.

To add functionality at certain points in the training process, a user can either subclass and overwrite the 'onNewEpisode_user', 'onStep_user', and 'onDone_user' methods,
    or, they can pass or set unbound methods in the userMethodsDict using the keys 'onNewEpisode', 'onStep', and 'onDone' which will be called by default
    and will be passed a reference to the instance of this RLExperiment class.


"""

import os
import time
from datetime import timedelta
from datetime import datetime
import numpy as np

class RLExperiment():

    def __init__(self, agent, environment, nEpisodes=1, cudaDevices="0", renderMode=None, resetEnvOnNewEpisode=True, callbacksDict = None):
        self.agent = agent
        self.env = environment
        self.nEpisodes = nEpisodes
        self.renderMode = renderMode
        self.resetEnvOnNewEpisode = resetEnvOnNewEpisode
        self.callbacks = callbacksDict
        self.totalTimeElapsed = 0
        self.state_size = self.env.getObservationSpaceSize()
        self.action_size = self.env.getActionSpaceSize()
        self.currentEpisode = 0
        self.done = False
        self.state = None
        self.next_state = None
        self.action = None
        self.reward = None
        self.info = None
        self.episodeStartTime = 0
        self.consoleLog = '\n\n=========\n\n'
        os.environ["CUDA_VISIBLE_DEVICES"]=cudaDevices #  '-1' = CPU,  '0,1' makes GPUs 0 and 1 visible.

    def run(self):
        """ starts training over nEpisodes """
        self.onExperimentStart()
        for self.currentEpisode in range(1,self.nEpisodes+1):
            self.onNewEpisode()
            self.runEpisode()
        self.onExperimentComplete()
        
    def onNewEpisode(self):
        """ this runs at the start of a new episode """
        self.consoleMsg('---> Starting Episode {}/{} <---'.format(self.currentEpisode,self.nEpisodes),topBorder=True)
        if self.resetEnvOnNewEpisode: self.envReset()
        self.done = False
        self.episodeStartTime = time.time()
        self.onNewEpisode_user()

    def onExperimentStart(self):
        """ called when experiment begins, before the first episode """
        self.consoleMsg("**Experiment Start**",topBorder=True)
    
    def onExperimentComplete(self):
        """ called when all episodes have finished """
        self.consoleMsg("--------> ALL episodes completed in {} | -- Saving Model -> {}".format(timedelta(seconds=self.totalTimeElapsed),self.env.getReportLogDir()),topBorder=True,bottomBorder=True)
        self.agent.save(self.env.getReportLogDir()+"/"+self.env.environmentID + '_ModelWeights.h5')
    
    def envReset(self):
        """ handles environment reset """
        self.state = self.env.reset()
        self.state = np.reshape(self.state, [1, self.state_size])

    def envRender(self):
        """ handles environement render if enabled """
        if self.renderMode != None: self.env.render(renderMode) 

    def runEpisode(self):
        """ this contains the content for each episode and is called each episode by self.run(); override if you need to add behavior to the episode, or change how often it is called. """
        self.mainUpdate()

    def mainUpdate(self):
        """ handles primary train/update sequence """
        self.envRender()
        self.action = self.agent.act(self.state)
        self.next_state, self.reward, self.done, self.info = self.env.step(self.action)
        self.next_state = np.reshape(self.next_state, [1, self.state_size])
        self.onPostStep_user()
        self.state = self.next_state
        if self.done: self.onDone()

    def onDone(self):
        """ called when an episode has ended """
        finishTime = time.time() - self.episodeStartTime
        self.totalTimeElapsed += finishTime
        nRemainingEpisodes = (self.nEpisodes - (self.currentEpisode))
        timeRemaining = (self.totalTimeElapsed/(self.currentEpisode)) * nRemainingEpisodes
        self.consoleMsg("Episode {} completed in {} seconds. | {} episodes ({}) remaining".format(self.currentEpisode,timedelta(seconds=finishTime),nRemainingEpisodes,timedelta(seconds=timeRemaining)))
        self.onDone_user()
        self.env.exportReportToCsv()
        self.saveConsoleLog()

    def consoleMsg(self,message, includeTime=True, topBorder=False, bottomBorder=False):
        """ message provided will be output to the console, and saved in a log to be exported when the experiment is complete."""
        timeNow = datetime.now().strftime("%H:%M:%S")
        msg = '{} | {}'.format(timeNow, message) if includeTime else message
        if topBorder: msg = '==============================\n' + msg
        if bottomBorder: msg += '\n=============================='
        self.consoleLog += '\n'+msg
        print(msg)

    def saveConsoleLog(self,path=None):
        """  saves contents of self.consoleLog to path; if path==None, the environment's reportLogDir is used. """
        if path==None: path = self.env.getReportLogDir() + '/consoleLog.txt'
        with open(path, 'a') as f: 
            f.write(self.consoleLog)

    #
    # User Callbacks handled below - the "..._user" methods can be overwritten when subclassing
    #

    def userCallBack(self,callbackKey):
        """ calls the given callbackKey and passes self """
        try:
            self.callbacks[callbackKey](self)
        except:
            pass

    def onNewEpisode_user(self):
        """ ccalled at the end of the built-in onNewEpisode() method """
        self.userCallBack('onNewEpisode')

    def onPostStep_user(self):
        """ called after env.step() in mainUpdate() """
        self.userCallBack('onPostStep')

    def onDone_user(self):
        """ called at the end of the built-in onDone() method """
        self.userCallBack('onDone')

