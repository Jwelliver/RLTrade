from RLTrade.RLComponents import StateFeatureSet
from ProjectComponents import stateFunctions as stateFeatures

def stateSet1(env):
    metadata = {'id': 'stateSet1', 'desc': 'Test set - Position Status, and Position Value as pct of Acc Bal'}
    t = StateFeatureSet.StateFeatureSet(envRef=env, setMetadata=metadata)
    t.add(stateFeatures.trader_positionStatus)
    t.add(stateFeatures.trader_currentPositionValueAsPctOfAccountBalance)
    return t