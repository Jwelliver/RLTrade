from RLTrade.RLComponents import RewardSet
from ProjectComponents import rewardFunctions as rewards

def pctChangeInAccValOnClose(env, timePenalty=-0.01):
    metadata = {'id': 'rewardSet1', 'desc': 'onBar: position_onClosed_posValAsPctChangeOfAcc; Optional: timepenalty'}
    t = RewardSet.RewardSet(envRef=env, setMetadata=metadata)
    t.add(rewards.position_onClosed_posValAsPctChangeOfAcc,kwargRef={'multiplier':100})
    if timePenalty!=0: 
        t.add(rewards.timePenalty,kwargRef={'timePenaltyValue':timePenalty})
    return t
