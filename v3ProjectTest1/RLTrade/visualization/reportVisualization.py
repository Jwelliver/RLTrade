#113019 Report Visualization 
"""
    This module will contain utility functions and scripts to interact with RLTradeReportPlotter for visualizing trade report logs
"""

import RLTradeReportPlotter
from matplotlib import pyplot as plt
from matplotlib.widgets import MultiCursor
import pandas as pd

def customTradeSimReportPlot_1(csvPath, tradeReportPlotter, figTitle='TradeReport', pauseOnShow=True):
    """ hardcoded custom plotter to allow me to pick which state features I want on the overview """
    trp = tradeReportPlotter
    reportDf = pd.read_csv(csvPath)
    trp.figCount+=1

    plt.figure(trp.figCount)
    plt.gcf().suptitle(figTitle)

    #self.plotStateFeatures(reportDf)
    overviewAx = trp.plotPrice(reportDf)
    overviewAx.plot(reportDf['barNum'].values, reportDf['c'].rolling(5).mean())
    overviewAx.plot(reportDf['barNum'].values, reportDf['c'].rolling(14).mean())

    trp.plotTrades(reportDf, overviewAx)
    trp.plotActions(reportDf)
    trp.plotReward(reportDf)
    trp.plotPositionSize(reportDf)
    trp.plotAccountValue(reportDf)
    trp.plotUnrealizedPL(reportDf)

    multiCursor = MultiCursor(plt.gcf().canvas,plt.gcf().axes, color='r', lw=1)
    plt.show(block=pauseOnShow)


def plotTradeSimReportByAgentName(agentName, simNumsToPlot):
    """ utility function to make it quick and easy to view multiple sim reports at the same time with minimal input """
    trPlotter = RLTradeReportPlotter.RLTradeReportPlotter()
    reportLogPath ='Y:/Python/Keras Practice/120819 - RL v3/v3ProjectTest1/reportLogs'
    for i in simNumsToPlot:
        p = '{}/{}/{}_{}.csv'.format(reportLogPath,agentName,agentName,i)
        figTitle = '{} s{}'.format(agentName,i)
        #trPlotter.plotTradeSimReportFromCsv(p,figTitle,pauseOnShow=False)
        customTradeSimReportPlot_1(p,trPlotter,figTitle,pauseOnShow=False)
    plt.show(block=True)
    #plt.close('all')



########################################################

'''
t = RLTradeReportPlotter.RLTradeReportPlotter()

tPath = './reportLogs/plotting_test/reportFile1.csv'
#df = pd.read_csv(tPath)

#n = 'C:/Users/Josh/OneDrive/Python/Keras Practice/101919 - RL/reportLogs/Courtney_Barnes/Courtney_Barnes_10.csv'
#t.plotTradeSimReportFromCsv(n)
'''

agentName = 'Phyllis_miller'
simsToPlot = list(range(1,16,1))
plotTradeSimReportByAgentName(agentName,simsToPlot)
