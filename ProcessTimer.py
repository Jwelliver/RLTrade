"""
122119
ProcessTimer

Will be used to track start and end times for given identifiers in order to log time elapsed for various parts of code.

"""
import time
import datetime
import collections

class ProcessTimer():
    def __init__(self):
        self.dt = datetime.datetime
        self.totals = {}
        self.openTimers = {}

    def start(self,id):
        """ starts a timer for id"""
        self.openTimers[id] = self.dt.now()

    def stop(self, id):
        """ ends the open timer for id and applies the results to self.totals """
        stopTime = self.dt.now()
        startTime = self.openTimers[id]
        self.openTimers.pop(id)
        total = stopTime - startTime
        if not id in self.totals: self.totals[id] = {'totalTime': datetime.timedelta(), 'timesRun': 0}
        self.totals[id]['totalTime'] += total
        self.totals[id]['timesRun'] += 1

    def getTotalTime(self,id):
        """ returns total time for id """
        return self.totals[id]['totalTime']
    
    def getTotalTimeStr(self, id, format='%H:%M:%S'):
        """ returns total time for id as string with given formatting """
        return str(self.getTotalTime(id))

    def getTotals(self,id):
        pass
    