#import DeepWellTrade



#import TradingAccount
#import Market
#import Assets
#import pandas as pd

from datetime import timedelta

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

#print((100/10)%11)

import numpy as np

print(np.nanmax([1,10,3,np.nan]))


