####################
# Entry and Exits
####################


def doNothing():
    """ take no action """
    pass

def enterLong(env):
    """ attempt to enter long position """
    env.tradingAccount.enterPosition(orderType='buy', allowExit=False)

def enterShort(env):
    """ attempt to enter short position """
    env.tradingAccount.enterPosition(orderType='sell', allowExit=False)

def enterLong_exitShort(env):
    """ attempt to enter new long position or exit an existing short position """
    env.tradingAccount.enterPosition(orderType='buy', allowExit=True)

def enterShort_exitLong(env):
    """ attempt to enter new short position or exit an existing long position """
    env.tradingAccount.enterPosition(orderType='sell', allowExit=True)

def exitCurrentPosition(tradingAccount):
    """ exit the current position if one exists """
    env.tradingAccount.exitPosition()

####################
# Position Sizing
####################

def increasePositionSize(env, positionSizeIncrement):
    """ increase position size by positionSizeIncrement  """
    env.tradingAccount.adjustPositionSize(positionSizeIncrement)

def decreasePositionSize(env, positionSizeIncrement):
    """ decrease position size by positionSizeIncrement  """
    positionSizeIncrement = -abs(positionSizeIncrement) # ensure correct sign
    env.tradingAccount.adjustPositionSize(positionSizeIncrement)