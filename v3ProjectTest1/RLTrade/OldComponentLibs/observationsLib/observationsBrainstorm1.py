"""
    11/30/19
    ObservationsBrainstorm1

    This module will act as a container for various observation/statefeature functions during development/testing

"""

def baseline1(tradingSim):
    """ returns 1 if current close is greater than previous close else 0 """
    currentBarNum = tradingSim.currentBarNum
    return int(tradingSim.ohlc[currentBarNum]['c'] > tradingSim.ohlc[currentBarNum - 1]['c']) if currentBarNum > 0 else 0 

