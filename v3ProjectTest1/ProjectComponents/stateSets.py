from RLTrade.RLComponents import StateFeatureSet
from ProjectComponents import stateFunctions as stateFeatures

def stateSet1(env):
    metadata = {'id': 'stateSet1', 'desc': 'Test set - Position Status, and Position Value as pct of Acc Bal'}
    t = StateFeatureSet.StateFeatureSet(envRef=env, setMetadata=metadata)
    #t.add(stateFeatures.trader_positionStatus)
    t.add(stateFeatures.trader_currentPositionValueAsPctOfAccountBalance)
    t.add(stateFeatures.asset_is6smaAboveClose)
    t.add(stateFeatures.asset_is6smaAbove12sma)
    return t

def stateSet2_taTest(env):
    metadata = {'id': 'stateSet2_taTest', 'desc': 'Test set - returns linregSlope of 5sma'}
    t = StateFeatureSet.StateFeatureSet(envRef=env, setMetadata=metadata)
    #t.add(stateFeatures.trader_positionStatus)
    t.add(stateFeatures.trader_positionSize)
    t.add(stateFeatures.trader_currentPositionValueAsPctOfAccountBalance)
    t.add(stateFeatures.ta_linregSlopeOfSma,kwargRef={'smaPeriod': 5,'slopePeriod': 5})
    t.add(stateFeatures.ta_linregSlopeOfSma,kwargRef={'smaPeriod': 14,'slopePeriod': 3})
    return t

def stateSet3_taWindowTest(env):
    metadata = {'id': 'stateSet3_taWindowTest', 'desc': 'Test set - returns 3 period window of rsi of linregSlope of 3sma and 5sma'}
    t = StateFeatureSet.StateFeatureSet(envRef=env, setMetadata=metadata)
    t.add(stateFeatures.trader_positionStatus)
    t.add(stateFeatures.trader_positionSize)
    t.add(stateFeatures.trader_currentPositionValueAsPctOfAccountBalance)
    t.add(stateFeatures.ta_rsiOfLinregSlopeOfSma,kwargRef={'smaPeriod':5,'slopePeriod':5, 'rsiPeriod':5,'multiplier':0.01, 'window': 2})
    t.add(stateFeatures.ta_rsiOfLinregSlopeOfSma,kwargRef={'smaPeriod':14,'slopePeriod':5, 'rsiPeriod':5,'multiplier':0.01, 'window': 2})
    return t

def stateSet4_close(env):
    metadata = {'id': 'stateSet4_close', 'desc': 'Test set - baseline to use pos val and close only'}
    t = StateFeatureSet.StateFeatureSet(envRef=env, setMetadata=metadata)
    t.add(stateFeatures.trader_currentPositionValueAsPctOfAccountBalance)
    t.add(stateFeatures.asset_getActiveAssetFeatures,kwargRef={'featuresList': ['c']})
    #t.add(stateFeatures.ta_rsiOfClose,kwargRef={'rsiPeriod':5,'multiplier':0.01, 'window': 1})
    return t


