from binance_api import Binance
import BinanceFunctions
import CreateIndicators
from IndicatorsStrategiesState import Indicatorstates
import DatabaseReadInsert
import math
import os


API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")


class Trading:
    def __init__(self, _df, _symbol, _interval, _profit, _buy=0, _stoploss=0, _sell=0, _wins=0,
                 _losses=0, _inTrade=False, _tradeEntry=[], _tradeExit=[]):
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


if __name__ == '__main__':
    # if tables not created yes than create
    Ninjabot = Binance(API_KEY=API_KEY, API_SECRET=API_SECRET)

    symnbol_list = BinanceFunctions.getTradingSymbols(Ninjabot)
    symnbol_list = BinanceFunctions.symbolfilter(
        pairs=symnbol_list, Ninjabot=Ninjabot)

    Data_base = DatabaseReadInsert.Database()
    accountinfo = Ninjabot.account()
    balances = accountinfo["balances"]
    indicator_name = ["rsi", "stochastic", "bb"]

    print(symnbol_list)

    print("time values: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M")
    print("hello good sir which bot do you want to use?")
    botid = input("Type bot id: ")
    interval = input("enter time: ")
    print("YOUR BALANCE IS")
    for symbol in balances:
        if symbol["asset"] == "USDT":
            print(symbol["free"] + " $")

    quantity = float(input("how much dollar will you be spending: "))

    # zero signifies false
    while Data_base.getData(botid=botid, what="intrade", where="bots") == "0":

        strategy = Data_base.getData(
            botid=botid, what="strategy", where="bots")

        for symbol in symnbol_list:
            if Data_base.getData(botid=botid, what="intrade", where="bots") == "1":
                break
            df = BinanceFunctions.getSymbolData(
                Ninjabot=Ninjabot, symbol=symbol, interval=interval)
            df = CreateIndicators.createIndicators(
                symbol=symbol, df=df, indicator_name=indicator_name)

            icurrent = len(df['close'])-1
            Indicators = Indicatorstates(
                _interval=interval, _df=df, _icurrent=icurrent)

            print("{} had an rsi of {}".format(symbol, df['rsi'][icurrent]))

            if Indicators.strategyState("rsi") == True:
                print('Profittarget')
                print(abs((df['close'][icurrent] + 2 *
                           abs((df['low'][icurrent - 1] - df['close'][icurrent])))))

                print('Price')
                print(df['close'][icurrent])

                print("percentage gap")
                print(abs((df['close'][icurrent] + 2 * abs((df['low']
                                                            [icurrent - 1] - df['close'][icurrent]))))/df['close'][icurrent])
                if abs((df['close'][icurrent] + 2 * abs((df['low'][icurrent - 1] - df['close'][icurrent]))))/df['close'][icurrent] < 1.01:
                    if df['close'][icurrent] > 0.1:
                        quantity = round(quantity/df['close'][icurrent], 5)
                        if quantity > 1:
                            quantity = round(quantity, 0)

                        print("{} had rsi:{} had fast:{} had slow: {} had price{}, had lowbol: {}".format(
                            symbol, df['rsi'][icurrent], df['fast'][icurrent], df['slow'][icurrent], df['close'][icurrent], df['low_boll'][icurrent]))

                        print(round(quantity/df['close'][icurrent], 4))

                        initiateOrderData = BinanceFunctions.placeOrder(
                            Ninjabot=Ninjabot, symbol=symbol, side="BUY", type="MARKET", quantity=quantity, price="426", test=False)

                        # calculates the profit target and than doubles the loss for the profit target
                        stoplosstarget = df['low'][icurrent-1]
                        profittarget = df['close'][icurrent] + 2 * \
                            abs((df['low'][icurrent - 1] - df['close'][icurrent]))

                        Data_base.insertOrdersPlaced(
                            botid=botid, initiateOrderData=initiateOrderData, profittarget=profittarget, stoplosstarget=stoplosstarget)
                        print("Congratulations you bought: " + symbol)

    # the price is irrelevant since market order but im too lazy to remove it sue me
    # also the 1 signifies true
    print(Data_base.getData(botid=botid, what="intrade", where="bots"))
    while Data_base.getData(botid=botid, what="intrade", where="bots") == "1":
        print("in")

        symbol = Data_base.getData(
            botid=botid, what='symbol', where="ordersPlaced")
        quantity = Data_base.getData(
            botid=botid, what='quantity', where="ordersPlaced")*0.99

        # formatting complanits
        quantity = round(quantity, 5)
        if quantity > 2:
            quantity = math.floor(quantity)
        print(symbol)
        print(quantity)
        # as the name indicates...
        df = BinanceFunctions.getSymbolData(
            Ninjabot=Ninjabot, symbol=symbol, interval=interval)

        # no need to creaete indicators right?
        df = CreateIndicators.createIndicators(
            symbol=symbol, df=df, indicator_name=indicator_name)

        # this is the latest candale's data in other words the one currenly unfolding
        icurrent = len(df['close'])-1

        print("going smoothely")
        if df['close'][icurrent] < Data_base.getData(botid=botid, what="stoplosstarget", where="ordersplaced"):

            exitOrderData = BinanceFunctions.placeOrder(
                Ninjabot=Ninjabot, symbol=symbol, side="SELL", type="MARKET", quantity=quantity, price="1337", test=False)
            Data_base.insertOrdersEnded(
                botid=botid, exitOrderData=exitOrderData)
            print("Congratulations you have ran a succesful test")

        elif df['close'][icurrent] > Data_base.getData(botid=botid, what="profittarget", where="ordersplaced"):

            exitOrderData = BinanceFunctions.placeOrder(
                Ninjabot=Ninjabot, symbol=symbol, side="SELL", type="MARKET", quantity=quantity, price="1337", test=False)
            Data_base.insertOrdersEnded(
                botid=botid, exitOrderData=exitOrderData)
            print("congratulations you have run a succesful test and made a profit")
        print(df['close'][icurrent])
        print(Data_base.getData(botid=botid,
                                what="profittarget", where="ordersplaced"))
