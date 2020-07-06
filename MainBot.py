from binance_api import Binance
import BinanceFunctions
import CreateIndicators
import BacktestingEnviorment
import DatabaseReadInsert

API_KEY = "RcNwmxsGSrqbDZKqniDb2G4v7gEdx1iCY6LQaa7pFLz9SV4M2nm8xIokQ1WqaNsB"
API_SECRET = "FvZiJDnTJ9El1TKz5eHpdFnB5TqMOXOvDe3YM63gYpRJH5Ne8C6PuiDDtZKxr0Nm"
if __name__ == '__main__':
    Ninjabot = Binance(API_KEY=API_KEY, API_SECRET=API_SECRET)

    symnbol_list = BinanceFunctions.getTradingSymbols(Ninjabot)
    symnbol_list = BinanceFunctions.symbolfilter(pairs=symnbol_list, Ninjabot=Ninjabot)

    indicator_name = ["bb", "stochastic", "rsi"]
    print("time values: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M")
    interval = input("enter time: ")
    interval = "15m"
    profit = 0
    accountinfo = Ninjabot.account()
    balances = accountinfo["balances"]

    for symbol in symnbol_list:
        print(symbol)
        df = BinanceFunctions.getSymbolData(Ninjabot=Ninjabot, symbol=symbol, interval=interval)
        df = CreateIndicators.createIndicators(symbol=symbol, df=df, indicator_name=indicator_name)

        test = BacktestingEnviorment.BacktestingEnviorments(_df=df, _symbol=symbol, _interval=interval, _profit=[0])
        test.Backtest()
        profit = profit + sum(test.profit) 
    print(profit)