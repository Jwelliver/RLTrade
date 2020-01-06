from RLTrade.RLComponents import StateFeatureGroup
from ProjectComponents import stateFunctions as stateFeatures

def stateSet1(env):
    metadata = {'id': 'stateSet1', 'desc': 'onBar:  '}
    t = ActionGroup.RewardGroup(envRef=env, groupMetaData=metadata)
    t.add(rewards.position_onClosed_posValAsPctChangeOfAcc)
    return t