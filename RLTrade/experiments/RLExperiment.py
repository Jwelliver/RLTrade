"""
120819
RLExperiment class

There's a lot of odd/discomforting global usage here, but it's the only way I saw fit to make it modular in my tired state.

To add functionality at certain points in the training process, a user can either subclass and overwrite the 'onNewEpisode_user', 'onStep_user', and 'onDone_user' methods,
    or, they can pass or set unbound methods in the userMethodsDict using the keys 'onNewEpisode', 'onStep', and 'onDone' which will be called by default
    and will be passed a reference to the instance of this RLExperiment class.


"""

import os

class RLExperiment():

    def __init__(self, agent, environment, nEpisodes=1, cudaDevices="0", renderMode=None, userMethodsDict = None):
        self.agent = agent
        self.env = environment
        self.nEpisodes = nEpisodes
        self.render = renderMode
        self.userMethods = userMethodsDict
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
        os.environ["CUDA_VISIBLE_DEVICES"]=cudaDevices #  '-1' = CPU,  '0,1' makes both GPUs visible.

    def run(self, nEpisodes = -1):
        """ starts training over nEpisodes """
        if nEpisodes == -1: nEpisodes = self.nEpisodes 
        self.onExperimentStart()
        for e in range(nEpisodes):
            self.onNewEpisode(resetEnv=True)
            self.mainUpdate()
            if self.done:
                self.onDone()
                break
        
    def onNewEpisode(self,resetEnv=True):
        """ this runs at the start of a new episode """
        print('===============================\n--------> Starting Episode {}/{}'.format(e+1,nEpisodes))
        self.episodeStartTime = time.time()
        if resetEnv: self.envReset()
        self.onNewEpisode_user()

    def onExperimentStart(self):
        """ called when experiment begins, before the first episode """
        print("Begin")
    
    def onExperimentComplete(self):
        """ called when all episodes have finished """
        print(" ======================== \n ----------> ALL episodes completed in {} | -- Saving Model -> {} \n========================".format(timedelta(seconds=self.totalTimeElapsed),env.getReportLogDir()))
        agent.save(env.getReportLogDir()+"/"+env.environmentID + '_ModelWeights.h5')
    
    def envReset(self):
        """ handles environment reset """
        self.state = env.reset()
        self.state = np.reshape(state, [1, self.state_size])

    def envRender(self):
        """ handles environement render if enabled """
        env.render(renderMode) if self.renderMode != None

    def mainUpdate(self, state):
        """ handles primary train/update sequence given the state and returns the next state """
        self.envRender()
        self.action = agent.act(self.state)
        self.next_state, self.reward, self.done, self.info = env.step(action)
        self.next_state = np.reshape(next_state, [1, self.state_size])
        self.onStep_user()
        self.state = next_state

    def onDone(self):
        """ called when an episode has ended """
        finishTime = time.time() - self.episodeStartTime
        totalTime += finishTime
        nRemainingEpisodes = (nEpisodes - (self.currentEpisode+1))
        timeRemaining = (totalTime/(self.currentEpisode+1)) * nRemainingEpisodes
        print("Episode {} completed in {} seconds. | {} episodes ({}) remaining".format(self.currentEpisode,timedelta(seconds=finishTime),nRemainingEpisodes,timedelta(seconds=timeRemaining)))
        print(info)
        self.onDone_user()

    #
    # Custom methods called below
    #

    def callUserMethod(self,userMethodKey):
        """ calls the given userMethodKey and passes self """
        try:
            self.userMethods[userMethodKey](self)
        except:
            pass

    def onNewEpisode_user(self):
        """ ccalled at the end of the built-in onNewEpisode() method """
        self.callUserMethod('onNewEpisode')

    def onStep_user(self):
        """ called after env.step() in mainUpdate() """
        self.callUserMethod('onStep')

    def onDone_user(self):
        """ called at the end of the built-in onDone() method """
        self.callUserMethod('onDone')

