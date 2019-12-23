'''
112819:
    RLTradeReportPlotter will be a class that allows visualization of experiment reports outputted by the TradingSim class for analysis.

===

MVP: 
Loads a report csv file into a dataframe, uses hardcoded plot types to show relevant data.

Later:
-implement mpl_finance for candlestick data

-alternative solutions:
    -TradingSim could export a separate file for each sim which details trade summaries from the TradePosition Class history.
        ...This would be a lot simpler & more flexible than parsing the data from the reportLog... and in this route, we could remove tradeData from the report log
        ... along with the messy code that it needs to be added while the sim is running.
        ... OR maybe keep it - ? might be useful to see all the data linearly, bar by bar rather than in two separate formats, only able to be visually combined with code.

===



'''
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


class RLTradeReportPlotter():
    
    def __init__(self):
        self.figCount = 0
        #plt.ion()

    def plotTradeSimReport(self,reportDf,figTitle='TradeSimReport',pauseOnShow=True):
        """ plots data from the provided report Dataframe """
        self.figCount+=1

        plt.figure(self.figCount)
        plt.gcf().suptitle(figTitle)

        #self.plotStateFeatures(reportDf)
        overviewAx = self.plotPrice(reportDf)
        self.plotTrades(reportDf, overviewAx)
        self.plotActions(reportDf)
        self.plotReward(reportDf)
        self.plotAccountValue(reportDf)
        
        plt.show(block=pauseOnShow)
    
    def addSubplot(self):
        """ adds a new subplot to current figure and adjusts the existing subplots to fit """
        cf = plt.gcf()
        currentNAxes = len(cf.get_axes())
        for i in range(currentNAxes):
            cf.axes[i].change_geometry(currentNAxes+1,1,i+1)
        return plt.subplot(currentNAxes+1,1,currentNAxes+1)

    def plotTradeSimReportFromCsv(self,csvPath,figTitle='TradeSimReport',pauseOnShow=True):
        """ loads given csv as dataframe and plots data """
        self.plotTradeSimReport(pd.read_csv(csvPath),figTitle=figTitle,pauseOnShow=pauseOnShow)

    def plotPrice(self, reportDf, ax=None):
        """ plots price data (close only) """
        if ax==None: ax=self.addSubplot()
        ax.set_title('Overview')
        ax.plot(reportDf['c'],'k')
        return ax

    def plotActions(self, reportDf, ax=None):
        """ plots action taken """
        if ax==None: ax=self.addSubplot()
        ax.set_title('Action Taken')
        actions = reportDf['action'].values
        bars = reportDf['barNum'].values
        sellMask = actions == 2
        buyMask = actions == 1
        naMask = actions == 0
        ax.scatter(bars[sellMask],actions[sellMask],color='r')
        ax.scatter(bars[buyMask],actions[buyMask],color='g')
        ax.scatter(bars[naMask],actions[naMask],color='b')
        return ax

    def plotReward(self, reportDf, ax=None):
        """ plots reward """
        if ax==None: ax=self.addSubplot()
        bars = reportDf['barNum'].values
        reward = reportDf['reward'].values
        sma = reportDf['reward'].rolling(window=10).mean()
        ax.set_title('Reward')
        mask1 = reward >= 0
        mask2 = reward < 0
        ax.bar(bars[mask1],reward[mask1],color='g')
        ax.bar(bars[mask2],reward[mask2],color='r')
        ax.plot(sma,':k')
        return ax

    def plotUnrealizedPL(self, reportDf, ax=None):
        """ plots unrealized PL """
        if ax==None: ax=self.addSubplot()
        bars = reportDf['barNum'].values
        upl = reportDf['unrealizedPL'].values
        sma = reportDf['unrealizedPL'].rolling(window=10).mean()
        ax.set_title('Unrealized PL')
        mask1 = upl >= 0
        mask2 = upl < 0
        ax.bar(bars[mask1],upl[mask1],color='g')
        ax.bar(bars[mask2],upl[mask2],color='r')
        ax.plot(sma,':k')
        return ax

    def plotAccountValue(self, reportDf, ax=None):
        """ plots account value """
        if ax==None: ax=self.addSubplot()
        ax.set_title('Account Value (equity)')
        ax.plot(reportDf['accountValue'],'b') 
        ax.plot(reportDf['accountBalance'],'k')
        return ax

    def plotAccountBalance(self, reportDf, ax=None):
        """ plots account value """
        if ax==None: ax=self.addSubplot()
        ax.set_title('Account Balance')
        ax.plot(reportDf['accountBalance'],'b') 
        return ax
    
    def plotStateFeatures(self,reportDf,stateFeatureTitleList=None, ax=None): #currently pretty rigid functionality; either will print all state features onto the given axis, or will plot them separately; todo: fix that; allow for specific state features; allow options for different plot types per feature
        """ plots state features - Assumes their headers are formatted as 'stateFeature_0',etc. If stateFeatureTitleList can be a list of strings which will correspond to each statefeature found and used as plot titles  """
        n = 0
        sfTitle = ''
        sfData = []
        axList = []
        while True:
            sfId = 'stateFeature_{}'.format(n)
            try:
                sfTitle = stateFeatureTitleList[n] #single line attempt to avoid try/except: sfTitle = sfId if len(stateFeatureTitleList) == 0 or len(stateFeatureTitleList) < n else stateFeatureTitleList[n]
            except:
                sfTitle = sfId
            if not sfId in reportDf.columns: break
            sfData = reportDf[sfId]
            sfAx = ax if ax!=None else self.addSubplot()
            sfAx.set_title(sfTitle)
            sfAx.scatter(reportDf['barNum'],sfData)
            axList.append(sfAx)
            n+=1
        return axList if len(axList) >= 1 else sfAx
            

    def plotTrades(self,reportDf, ax=None):
        """ plots trades onto main subplot """
        if ax==None: ax=self.addSubplot()
        for i in self.getTradeSummary(reportDf).to_dict(orient='records'):
            entPrice = i['entryPrice']
            entBar = i['entryBarNum']
            exPrice = i['exitPrice']
            exBar = i['exitBarNum']
            entryArrow = ('^' if i['positionType'] == 1 else 'v') + 'g'
            exitArrow = ('v' if i['positionType'] == 1 else '^') + 'r'
            if exPrice != np.nan:
                tradeLineColor = '--b' if i['positionType'] == 1 else '--y'
                ax.plot([entBar,exBar],[entPrice,exPrice],tradeLineColor) #trade line
                ax.plot(exBar,exPrice,exitArrow) #exit marker
                #plt.text(exBar,exPrice,'{}'.format(i['tradeNum'])) #exit text
            ax.plot(entBar,entPrice,entryArrow) #entry marker
            ax.text(entBar,entPrice,'{}'.format(i['tradeNum'])) #entry text

    def getTradeSummary(self, reportDf):
        """ returns a df with data on each trade: [tradeNum,positiontype,entryBarNum,entryPrice,exitBarNum,exitPrice] """
        tradeList = []
        ent = reportDf.dropna(subset=['entryPrice'])
        ex = reportDf.dropna(subset=['exitPrice'])
        for i in range(len(ent)):
            d= {}
            d['tradeNum'] = str(i) #or can use ent.iloc[i]['nTrades']
            d['positionType'] = ent.iloc[i]['positionStatus']
            d['entryBarNum'] = ent.iloc[i]['barNum']
            d['entryPrice'] = ent.iloc[i]['entryPrice']
            if(i>len(ex)-1):
                d['exitBarNum'] = np.nan
                d['exitPrice'] = np.nan
            else:
                d['exitBarNum'] = ex.iloc[i]['barNum']
                d['exitPrice'] = ex.iloc[i]['exitPrice']
            tradeList.append(d)
        return pd.DataFrame(tradeList)


    def getCustomReportPlot(self,reportDf,reportList,reportOptionsDict=None):
        """ (Untested - just getting the idea out) quick idea to modularize the plot output - reportList contains specified strings which correlate the plot functions called; the options dict is the specific string as a key and values is list of args for the func"""
        self.nSubplots = len(reportList)
        n = 0
        for i in reportList:
            try:
                args = reportOptionsDict[i] or ""
            except:
                args = ""
            plt.subplot(self.nSubplots,1,n)
            exec('self.plot{}(reportDf,{})'.format(i,args))
            n+=1
    


############## Testing ################

'''
t = RLTradeReportPlotter()

tPath = './reportLogs/plotting_test/reportFile1.csv'
#df = pd.read_csv(tPath)

#n = 'C:/Users/Josh/OneDrive/Python/Keras Practice/101919 - RL/reportLogs/Courtney_Barnes/Courtney_Barnes_10.csv'
#t.plotTradeSimReportFromCsv(n)
'''
