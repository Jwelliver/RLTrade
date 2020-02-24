from RLTrade.RLComponents import ActionSet
from ProjectComponents import actionFunctions as actions

def longOnly(env, positionSizeIncrement = 100, variablePositionSize=True):
    metadata = {'id': 'longOnly_staticPositionSize', 'desc': 'Do nothing; Enter Long; Exit; Optional: inc pos size, dec pos size'}
    t = ActionSet.ActionSet(envRef=env, setMetadata=metadata)
    t.add(actions.doNothing)
    t.add(actions.enterLong)
    t.add(actions.exitCurrentPosition)
    if variablePositionSize:
        t.add(actions.increasePositionSize,kwargRef={'positionSizeIncrement': positionSizeIncrement})
        t.add(actions.decreasePositionSize,kwargRef={'positionSizeIncrement': positionSizeIncrement})
    return t

def longShort(env,positionSizeIncrement=100,variablePositionSize=True):
    metadata = {'id': 'longShort', 'desc': 'Do nothing; Enter Long; Enter Short; Exit Pos; Optional: inc pos size, dec pos size'}
    t = ActionSet.ActionSet(envRef=env, setMetadata=metadata)
    t.add(actions.doNothing)
    t.add(actions.enterLong)
    t.add(actions.enterShort)
    t.add(actions.exitCurrentPosition)
    if variablePositionSize:
        t.add(actions.increasePositionSize,kwargRef={'positionSizeIncrement': positionSizeIncrement})
        t.add(actions.decreasePositionSize,kwargRef={'positionSizeIncrement': positionSizeIncrement})
    return t
