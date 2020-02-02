"""
122819
RLComponentSet.py

Parent Class to Component Sets of specific types
"""

from RLTrade.RLComponents.RLComponent import RLComponent


class RLComponentSet:
    def __init__(self, componentList=[],envRef=None,setMetadata={}):
        self.componentList = componentList
        self.env = envRef
        self.metadata = setMetadata
    
    def getComponentMetaData(self):
        """ returns a list of metadata dicts ordered by component """
        return [i.metadata for i in self.componentList]

    def add(self,callback,id=None,description=None,kwargRef={},metadata={}):
        """ creates RLComponent from a given function """
        kwargRef['env'] = self.env #ensure env reference is included
        t = RLComponent(callback=callback,id=id,description=description,kwargRef=kwargRef,metadata=metadata)
        self.componentList.append(t)
        