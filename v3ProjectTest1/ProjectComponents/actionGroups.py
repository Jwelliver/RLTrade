from RLTrade.RLComponents import ActionGroup
from ProjectComponents import actionFunctions as actions

def longOnly_variablePositionSize(env, positionSizeIncrement = 100):
    metadata = {'id': 'longOnly_variablePositionSize', 'desc': 'Do nothing; Enter Long; Exit; Increase Position Size; Decrease Position Size '}
    t = ActionGroup.ActionGroup(envRef=env, groupMetaData=metadata)
    t.add(actions.doNothing)
    t.add(actions.enterLong)
    t.add(actions.exitCurrentPosition)
    t.add(actions.increasePositionSize,kwargRef={'positionSizeIncrement': positionSizeIncrement})
    t.add(actions.decreasePositionSize,kwargRef={'positionSizeIncrement': positionSizeIncrement})
    return t