"""
122819
RLComponentGroup.py

"""

from RLTrade.RLComponents import RLComponent


class RLComponentGroup:
    def __init__(self, componentList=[],envRef=None,groupMetadata={}):
        self.componentList = componentList
        self.env = envRef
        self.metadata = groupMetadata

    def addFunc(self,callback,id=None,description=None,kwargRef={},metadata={}):
        """ creates RLComponent from a given function """
        kwargRef['env'] = self.env #ensure env reference is included
        t = RLComponent(callback=callback,id=id,description=description,kwargRef=kwargRef,metadata=metadata)
        self.componentList.append(t)
        