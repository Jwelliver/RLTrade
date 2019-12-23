# Deep Q-learning Agent
#from https://keon.io/deep-q-learning/
import random
import gym
import numpy as np
from collections import deque
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import multiprocessing as mp

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=5000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
        self.nReplaysDebug = 0
        self.nFitCalls = 0

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(12, input_dim=self.state_size, activation='relu'))
        model.add(Dense(12, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action
    
    def replayParallel(self, batch_size):
        """ calls replay in parallel processing"""
        pool = mp.Pool(mp.cpu_count())
        minibatch = random.sample(self.memory, batch_size)

        n = 0
        self.nReplaysDebug+=1

        pool.starmap(self.singleReplay,minibatch)
        
        # pool.apply approach
        #for state, action, reward, next_state, done in minibatch:
        #    pool.apply(self.singleReplay,args=(state,action,reward,next_state,done))
        #    #n+=1

        pool.close()
        pool.join()
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def singleReplay(self,state,action,reward,next_state,done):
        """ single replay loop to be used in multiprocessing """
        target = reward
        if not done:
            target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
        target_f = self.model.predict(state)
        target_f[0][action] = target
        self.model.fit(state, target_f, epochs=1, verbose=0)

    def replay_orig(self, batch_size):
        """ original replay method """
        minibatch = random.sample(self.memory, batch_size)
        n = 0
        self.nReplaysDebug+=1
        #print("DQNAgent.replay -> nReplays: {}".format(self.nReplaysDebug))
        for state, action, reward, next_state, done in minibatch:
            #print("DQNAgent.replay -> {}-{}".format(self.nReplaysDebug,n))
            target = reward
            if not done:
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
            n+=1
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)