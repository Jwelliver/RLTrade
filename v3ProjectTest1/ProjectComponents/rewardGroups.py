from RLTrade.RLComponents import RewardGroup
from ProjectComponents import rewardFunctions as rewards

def rewardSet1(env):
    metadata = {'id': 'rewardSet1', 'desc': 'onBar: position_onClosed_posValAsPctChangeOfAcc '}
    t = RewardGroup.RewardGroup(envRef=env, groupMetaData=metadata)
    t.add(rewards.position_onClosed_posValAsPctChangeOfAcc)
    return t