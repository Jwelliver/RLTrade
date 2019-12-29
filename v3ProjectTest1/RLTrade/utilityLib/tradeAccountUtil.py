"""
121519
tradeAccountUtil.py

Contains useful and common methods for working with the TradingAccount class.

"""


def getPositionValAsPctOfAccountVal(self,account,position=None): #TODO 121519: 
    """ returns the given position value as a percent of the account value; if position==None, currentPosition will be used; if no current position exists, 0 is returned. """
    #This is not complete - I realized that, to handle any position check, you'll need to determine the accountVal at the position's entryBar and exitBar, and compare; but
    # ... I don't currently true the account log, so I'm skipping this and creating a new method for currentPosition checks only.
    pos = position if position != None else account.getCurrentPosition()
    if pos==None: return 0
    posVal = pos.getPositionValue()
    return posVal / (account.getAccountValue() - posVal)