from RLTrade.RLComponents import RewardSet
from ProjectComponents import rewardFunctions as rewards

def rewardSet1(env):
    metadata = {'id': 'rewardSet1', 'desc': 'onBar: position_onClosed_posValAsPctChangeOfAcc '}
    t = RewardSet.RewardSet(envRef=env, setMetadata=metadata)
    t.add(rewards.position_onClosed_posValAsPctChangeOfAcc)
    return t