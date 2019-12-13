#import DeepWellTrade



#import TradingAccount
#import Market
#import Assets
#import pandas as pd

'''
a = Assets.FXAsset(pd.DataFrame())
m = Market.Market([a])

t = TradingAccount.TradingAccount(m,1000)

t.adjustBalance(-100)

t.reset()

print(t.accountBalance)
'''

#df = pd.DataFrame()

#df.iloc[2]['testKey'] = 1.123
#f.loc[2,'testKey'] = 1.123

#t = {'k1': 1.1, 'k2': 2.2}

#df.loc[1] = t

#print(df)

'''
for k,v in dsadsa.items():
    print(k)
    print(v)
    #print('k={} | v={}'.format(k,v))'''



class Rect():
    def __init__(self, w, h):
        self.w = w
        self.h = h
    

class Square(Rect):
    def __init__(self,**kwds):
        super().__init__(**kwds)


t = Square(w=10,h=20)

print("w: {} h: {}".format(t.w,t.h))