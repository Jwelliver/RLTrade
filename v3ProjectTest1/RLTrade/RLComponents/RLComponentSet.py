"""
122819
RLComponentSet.py

Parent Class to Component Sets of specific types
"""

from RLTrade.RLComponents.RLComponent import RLComponent


class RLComponentSet:
    def __init__(self, componentList=None,envRef=None,setMetadata=None):
        if setMetadata==None: setMetadata={}
        self.componentList = [] if componentList==None else componentList
        self.env = envRef
        self.metadata = setMetadata
    
    def getComponentMetaData(self):
        """ returns a list of metadata dicts ordered by component """
        return [i.metadata for i in self.componentList]

    def add(self,callback,id=None,description=None,kwargRef=None,metadata=None):
        """ creates RLComponent from a given function;  """
        if metadata==None: metadata = {}
        if kwargRef==None: kwargRef = {}
        kwargRef['env'] = self.env #ensure env reference is included
        t = RLComponent(callback=callback,id=id,description=description,kwargRef=kwargRef,metadata=metadata)
        self.componentList.append(t)
        