"""
120819
RLExperiment class

There's a lot of odd/discomforting global usage here, but it's the only way I saw fit to make it modular in my tired state.
"""

import os


class RLExperiment():

    def __init__(self, agent, environment, nEpisodes=1, cudaDevices="0", renderMode=None):
        self.agent = agent
        self.env = environment
        self.nEpisodes = nEpisodes
        self.render = render
        self.totalTimeElapsed = 0
        self.state_size = self.env.getObservationSpaceSize()
        self.action_size = self.env.getActionSpaceSize()
        self.currentEpisode = 0
        self.done = False
        self.state = None
        self.action = None
        self.reward = None
        self.info = None
        self.episodeStartTime = 0
        os.environ["CUDA_VISIBLE_DEVICES"]=cudaDevices #  '-1' = CPU,  '0,1' makes both GPUs visible.

    def run(self):
        """ starts training over nEpisodes """
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
        #userOnNewEpisode_Callback

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
        next_state, self.reward, self.done, self.info = env.step(action)
        next_state = np.reshape(next_state, [1, self.state_size])
        self.postStep()
        #agent.remember(state, action, reward, next_state, done)
        self.state = next_state
        
    def postStep(self):
        """ called after env.step() in mainUpdate(); overwrite, or use callback """
        #postStep_user callback
        pass

    def onDone(self):
        """ called when an episode has ended """
        finishTime = time.time() - self.episodeStartTime
        totalTime += finishTime
        nRemainingEpisodes = (nEpisodes - (self.currentEpisode+1))
        timeRemaining = (totalTime/(self.currentEpisode+1)) * nRemainingEpisodes
        print("Episode {} completed in {} seconds. | {} episodes ({}) remaining".format(self.currentEpisode,timedelta(seconds=finishTime),nRemainingEpisodes,timedelta(seconds=timeRemaining)))
        print(info)
        #onDone_user callback