"""
122819
RLComponent.py

Provides a structure to represent a single function which can be used as a state, action, or reward in an RLExperiment

-needs callback or overridable method
-needs a container for params, references, etc.
"""
import inspect

class RLComponent:

    def __init__(self,callback,id=None,description=None,kwargRef={},metadata={}):
        """ callback is the function this component represents; if none, you must override self.call(), use kwargRef to init any params on the callback (i.e. by setting obj references)"""
        self.callback = callback
        self.id = id if id!=None else callback.__name__
        self.description = description if description!=None else callback.__doc__
        self.argDict = self._buildArgDict()
        self.argDict.update(kwargRef)
        self.metadata = metadata
        self.enabled = True

    def call(self, **kwargs):
        """ calls component callback and returns any values """
        self.argDict.update(kwargs)
        if self.enabled: return self.callback(**self.getArgs())

    
    def getArgs(self):
        """ processes args from argList """
        #here, you'd maybe check for any callback args and call them, then compile a final list of args to be used when calling the callback
        return self.argDict

    def _buildArgDict(self):
        """ generates and returns argDict from self.callback's arguments """
        t = inspect.getfullargspec(self.callback)
        args = t.args
        defaultVals = t.defaults
        nArgsWithoutDefaultVal = len(args) - len(defaultVals)
        argDict = {i: None for i in args[:nArgsWithoutDefaultVal]}
        argDict.update({args[nArgsWithoutDefaultVal:][i]: defaultVals[i] for i in range(len(defaultVals))})
        return argDict
        