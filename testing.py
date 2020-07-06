from binance_api import Binance
import BinanceFunctions
import CreateIndicators
import BacktestingEnviorment
import DatabaseReadInsert

API_KEY = "RcNwmxsGSrqbDZKqniDb2G4v7gEdx1iCY6LQaa7pFLz9SV4M2nm8xIokQ1WqaNsB"
API_SECRET = "FvZiJDnTJ9El1TKz5eHpdFnB5TqMOXOvDe3YM63gYpRJH5Ne8C6PuiDDtZKxr0Nm"

Ninjabot = Binance(API_KEY=API_KEY, API_SECRET=API_SECRET)   

accountinfo = Ninjabot.account()
balances = accountinfo["balances"]
billion = 58564454.4154554645
print(round(billion, 2))
ding = 'mcoustd'
if ding[-4:] == "ustd":
    print(ding[-4:] == 'ustd')
