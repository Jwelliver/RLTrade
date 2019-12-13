"""
120819
Main.py

main for v3
"""


###############
 # Data Prep
###############

assetData = assetDataLib.baseLineData1()

####################
 # Environment Setup
####################

#tradeReportPlot = RLTradeReportPlotter.RLTradeReportPlotter()

testAsset = Assets.FXAsset(assetData)

market = Market.Market([testAsset])
account = TradingAccount.TradingAccount(market,initialBalance=10000)
rlTradeController = RLTradeController.RLTradeController(account,market)

env = TradeEnv.TradingEnv(rlTradeController)
state_size = env.getObservationSpaceSize()
action_size = env.getActionSpaceSize()

agent = DQNAgent(state_size, action_size)

batch_size = 32 #for replay
nBarsPerReplay = 5 # this is how many bars between each agent replay call. The lower the number, the more often it's called (slower)
