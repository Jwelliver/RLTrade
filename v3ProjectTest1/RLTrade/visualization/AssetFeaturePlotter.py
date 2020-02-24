"""
022220
AssetFeaturePlotter.py
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Cursor, MultiCursor

class AssetFeaturePlotter():
    """ Allows user to easily create a plot for price series, indicators, and other features. Also allows visualization of labels from a clusterer. """
    def __init__(self):
        self.figCount = 0

    def plot(self,*data,ax=None, colors=[], useIntBasedXAxis=True):
        """ plots each data on the ax given. If ax=None, the data will be added to a new subplot """
        if ax==None: ax = self.addSubplot()
        for i in range(len(data)):
            d = data[i]
            color = None if len(colors) <= i else colors[i]
            x = None if not useIntBasedXAxis else list(range(len(d)))
            ax.plot(x,d,color=color) if x!=None else ax.plot(d,color=color)
        return ax

    def plotFromDict(self,plotDict,useIntBasedXAxis=True):
        """ takes a specialized dict with keys as ints and values as sub-dicts containing "data" and "colors" keys; ie. {0: {'data': [d1,d2], 'colors': ['k']}, 1: {'data':[d3], 'colors': ['b']}}"""
        for i in range(len(plotDict.items())):
            data = plotDict[i]['data']
            colors = [] if 'colors' not in plotDict[i] else plotDict[i]['colors']
            self.plot(*data, colors=colors, useIntBasedXAxis=useIntBasedXAxis)


    def addSubplot(self, shareXAxis=True):
        """ adds a new subplot to current figure and adjusts the existing subplots to fit """
        cf = plt.gcf()
        currentNAxes = len(cf.get_axes())
        for i in range(currentNAxes): cf.axes[i].change_geometry(currentNAxes+1,1,i+1)
        sharedAxis = None if not shareXAxis or currentNAxes == 0 else plt.gcf().axes[0]
        return plt.subplot(currentNAxes+1,1,currentNAxes+1,sharex=sharedAxis)

    def plotClusterLabels(self, labels, alpha=0.3):
        """ plots across all axes a background with a different color for each label; labels should be a list of len(nBarsInPlot) size with a labels for each bar """
        colorList = plt.cm.rainbow(np.linspace(0,1,np.amax(labels)+1))
        for i in plt.gcf().axes:
            for ii in range(0,len(labels)):
                label = labels[ii]
                color = colorList[label]
                i.axvspan(ii, ii+1, color=color, alpha=alpha)

    def showPlot(self):
        """ shows plot """
        multiCursor = MultiCursor(plt.gcf().canvas,plt.gcf().axes, color='r', lw=1)
        plt.show()