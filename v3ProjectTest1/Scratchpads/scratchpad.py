#import DeepWellTrade



#import TradingAccount
#import Market
#import Assets
#import pandas as pd

from datetime import timedelta
import numpy as np

'''def experimentTimeEstimate(nBars,batch_size,nBarsPerReplay, nEpisodes): #incomplete - need to calc for added time per episode
    """ quick rough estimate of time to complete """
    # (((nbars/100)*7.1) + (batch_size*5))/nBarsPerReplay
    ans1 = (((nBars*0.021) + (batch_size*5))/nBarsPerReplay)*nEpisodes
    ans2 = ((((nBars/100)*7.1) + ((batch_size-1)*5))/nBarsPerReplay)*nEpisodes
    return ans1,ans2

t1,t2 = experimentTimeEstimate(nBars=500,batch_size=32,nBarsPerReplay=3,nEpisodes=50)
print(timedelta(seconds=t1))
print(timedelta(seconds=t2))

'''

'''from RLTrade import TradePosition
from RLTrade import Assets
import pandas as pd

posSize = 1000

a = Assets.FXAsset(pd.DataFrame())
t = TradePosition.TradePosition(a,'buy',posSize,1,1)

print(t.positionSize)
posSize = 100000
print(t.positionSize)'''


'''
import ProcessTimer
t = ProcessTimer.ProcessTimer()

t.start('test1')
for i in range(1,100000):
    y = 9 + 7

t.stop('test1')

print(t.getTotalTimeStr('test1'))
'''

import inspect
#print((100/10)%11)

def test1(**a):
    d = {'k1': 'v1', 'k2': 'v2'}
    d.update(a)
    #print(d)

def test2(a,b):
    pass

def test3(a,b=34):
    pass

def test4(a=20,b=34):
    pass

def test5(a,b=34,*kwargs, t):
    pass

def test6(*args,t=None):
    for i in args:
        print(i)

test6([11,12],[21,22])

def argDict(func):
    t = inspect.getfullargspec(func)
    args = t.args
    defaultVals = t.defaults
    nArgsWithoutDefaultVal = len(args) - len(defaultVals)
    argD = {i: None for i in args[:nArgsWithoutDefaultVal]}
    argD.update({args[nArgsWithoutDefaultVal:][i]: defaultVals[i] for i in range(len(defaultVals))})
    print(argD)
    #argD = {*t['args']}


def nnZeroesTest():
    from keras.models import Sequential
    from keras.layers import Dense
    from keras.optimizers import Adam
    from keras.utils import plot_model
    model = Sequential()
    model.add(Dense(5, input_dim=3, activation='relu'))
    model.add(Dense(5, activation='relu'))
    model.add(Dense(3, activation='linear'))
    model.compile(loss='mse', optimizer=Adam(lr=0.01))

    in0 = np.array([[0,0,0]])
    in1 = np.array([[1,1,1]])

    out0 = np.array([[0,0,0]])

    #plot_model(model,to_file='testModel_postInit.png')
    print(model.get_weights())
    pred1=model.predict(in0)
    print("prediction 0: {}".format(pred1))
    model.fit(in0,out0)
    #plot_model(model,to_file='testModel_postTrain_0.png')
    print(model.get_weights())
    pred1=model.predict(in1)
    print("prediction 1: {}".format(pred1))
    model.fit(in1,out0)
    #plot_model(model,to_file='testModel_postTrain_1.png')
    print(model.get_weights())



t = ['one',2,3.14]


v = 9
print(hasattr(v,'__iter__'))
t.extend(*v)

print(t)