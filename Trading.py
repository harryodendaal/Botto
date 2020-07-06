from binance_api import Binance
import BinanceFunctions
import CreateIndicators
from IndicatorsStrategiesState import Indicatorstates
import DatabaseReadInsert

API_KEY = "RcNwmxsGSrqbDZKqniDb2G4v7gEdx1iCY6LQaa7pFLz9SV4M2nm8xIokQ1WqaNsB"
API_SECRET = "FvZiJDnTJ9El1TKz5eHpdFnB5TqMOXOvDe3YM63gYpRJH5Ne8C6PuiDDtZKxr0Nm"
class Trading:
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

if __name__ == '__main__':
        Ninjabot = Binance(API_KEY=API_KEY, API_SECRET=API_SECRET)

        symnbol_list = BinanceFunctions.getTradingSymbols(Ninjabot)
        symnbol_list = BinanceFunctions.symbolfilter(pairs=symnbol_list, Ninjabot=Ninjabot)

        Data_base = DatabaseReadInsert.Database(_user="nativeuser", _database='bot_data', _password='365Pass')
        accountinfo = Ninjabot.account()
        balances = accountinfo["balances"]
        indicator_name = ["rsi"]

        print(symnbol_list)

        print("time values: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M")
        print("hello good sir which bot do you want to use?")
        botid = input("Type bot id: ")
        interval = input("enter time: ")
        print("YOUR BALANCE IS")
        for symbol in balances:
            if symbol["asset"] == "USDT" :
                print(symbol["free"] + " $")
        quantity = float(input("how much dollar will you be spending: "))

        while Data_base.getData(botid=botid, what="intrade", where="bots") == "false":
            strategy = Data_base.getData(botid=botid, what="strategy", where="bots")
            for symbol in symnbol_list:
                df = BinanceFunctions.getSymbolData(Ninjabot=Ninjabot, symbol=symbol, interval=interval)
                df = CreateIndicators.createIndicators(symbol=symbol, df=df, indicator_name=indicator_name)
                icurrent = len(df['close'])-1
                Indicators = Indicatorstates(_interval=interval, _df=df, _icurrent=icurrent)
                print(str(symbol) + " has an ris of: "  + str(df['rsi'][icurrent]))

                if Indicators.rsiOverSold() == True:
                    if df['close'][icurrent] > 0.1:
                        quantity = round(quantity/df['close'][icurrent],4)
                        if quantity > 1:
                            quantity = round(quantity,0)
                            
                        print(str(symbol) + " has an ris of: "  + str(df['rsi'][icurrent]))

                        print(round(quantity/df['close'][icurrent],4))
                        initiateOrderData = BinanceFunctions.placeOrder(Ninjabot=Ninjabot, symbol=symbol, side="BUY",type="MARKET", quantity=quantity,price="426",test= False)
                        stoplosstarget = df['low'][icurrent-1]
                        profittarget = df['close'][icurrent] + 2*abs((df['low'][icurrent - 1] - df['close'][icurrent]))
                        Data_base.insertOrdersPlaced(botid=botid, initiateOrderData=initiateOrderData, profittarget=profittarget, stoplosstarget=stoplosstarget)
                        print("Congratulations you bought: " + symbol)

        while Data_base.getData(botid=botid, what="intrade", where="bots") == "true":
            if df['close'][icurrent] < Data_base.getData(botid=botid, what="stoplosstarget", where="ordersplaced"):
                exitOrderData = BinanceFunctions.placeOrder(Ninjabot=Ninjabot, symbol=symbol, side="SELL",type="MARKET", quantity=quantity,price="1337",test= False)
                Data_base.insertOrdersEnded(botid=botid, exitOrderData=exitOrderData)
                print("Congratulations you have ran a succesful test")
            elif df['close'][icurrent] > Data_base.getData(botid=botid, what="profittarget", where="ordersplaced"):
                exitOrderData = BinanceFunctions.placeOrder(Ninjabot=Ninjabot, symbol=symbol, side="SELL",type="MARKET", quantity=quantity,price="1337",test= False)
                Data_base.insertOrdersEnded(botid=botid, exitOrderData=exitOrderData)
                print("congratulations you have run a succesful test and mate a profit")



                        
