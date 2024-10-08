import time

import IndicatorsStrategiesState as ISS
import PlotData
TOTALPROFIT = 0
class BacktestingEnviorments:

    def __init__(self, _df, _symbol, _interval, _profit, _buy = 0, _stoploss = 0, _sell = 0, _wins = 0,
                 _losses = 0, _inTrade=False, _tradeEntry=[], _tradeExit=[]):
        self.df = _df
        self.symbol = _symbol
        self.interval = _interval
        self.buy = _buy
        self.stoploss = _stoploss
        self.sell = _sell
        self.profit = _profit
        self.wins = _wins
        self.losses = _losses
        self.in_trade = _inTrade
        self.entryprices = _tradeEntry
        self.exitprices = _tradeExit
    


    def Backtest(self):
        self.exitprices = []
        self.entryprices = []
        for i in range(15, len(self.df['close']) - 1):

            Indicators =  ISS.Indicatorstates(_interval=self.interval, _df=self.df, _icurrent=i)

            if self.in_trade == False:
                if  Indicators.strategyState("beast"):
                    self.entryprices.append([self.df['time'][i + 1], self.df['open'][i + 1]])
                    self.stoploss = self.df["low"][i]
                    self.buy = self.df["open"][i + 1]
                    self.in_trade = True

            if self.in_trade == True:
                self.Checkforfail(i=i)
            if self.in_trade == True:
                self.CheckforSuccess(i=i)

        # if(abs(sum(self.profit)) > 0):
        self.ShowProfit()
        #     plot = PlotData.PlotGraph(_df=self.df, _symbol=self.symbol,
        #                             _entry_signal=self.entryprices, _exit_signal=self.exitprices)
        #     plot.plotGraph()
        time.sleep(2)


    def Checkforfail(self, i):
        if self.df['low'][i+1] < self.stoploss:
            self.profit.append((self.stoploss - self.buy) / self.buy * 100)
            self.exitprices.append([self.df['time'][i + 1], self.buy * (1 + (self.stoploss - self.buy) / self.buy)])
            self.losses = self.losses + 1
            self.in_trade = False

    def CheckforSuccess(self, i):
        if (self.df["high"][i + 1] - self.buy)/self.buy > 2* (self.buy - self.stoploss)/self.buy:
            self.profit.append(2*abs((self.stoploss - self.buy))/ self.buy * 100)

            self.exitprices.append([self.df['time'][i + 1], self.buy * (1 + 2*abs((self.stoploss - self.buy)) / self.buy)])
            self.wins = self.wins + 1
            self.in_trade = False

    def ShowProfit(self):
        gain = sum(self.profit)
        tradesmade = self.wins + self.losses
        if self.losses !=0:
            winrate = self.wins/tradesmade
        else:
            winrate  = 1
        

        print(f"Percentage made with longs on  {self.symbol} : {gain}")
        print(f"{tradesmade} trades made with a winrate of {winrate*100}")


        #for backtesting get the df and then 
        # move all rri.... those things one 
        # forward so that they indicate the 
        # values at the beginning of the candle 
        # than use those values to predict wherthe
        #  or not the current candle will be profitable 
        # and also what the percentage chaneg is that it
        #  will be succesful so that our model choose the
        #  most likely ones too suuccecd for the firs 29 
        # sekonds of the next candle than takes the trade