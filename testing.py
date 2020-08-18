from binance_api import Binance
import BinanceFunctions
import CreateIndicators
import BacktestingEnviorment
import DatabaseReadInsert
import datetime
import os
from BinanceFunctions import getSymbolData
API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")


Ninjabot = Binance(API_KEY=API_KEY, API_SECRET=API_SECRET)

print(getSymbolData(Ninjabot, "ETHUSDT", "15m", latest=True))