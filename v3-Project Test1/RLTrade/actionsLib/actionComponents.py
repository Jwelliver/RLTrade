"""
    12/22/19
    actionComponents.py

        -modular action functions which include the metadata format
        -all component funcs must include 'getMetadata' param, which is a dict with at least {'name': "", 'desc': ""}
            - 'name': general short string that may be used as header in dataframe, or graph,, etc.
            - 'desc': general description of the function's return values.
"""



def doNothing(getMetadata=False):
    """ take no action """
    if getMetadata: return {'name': 'doNothing', 'desc': 'Agent takes no action.'}

def enterLong(getMetadata=False):
    """ attempt to enter long position """