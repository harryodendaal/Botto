import pandas as pd
import requests
import json
import time


def getTradingSymbols(Ninjabot):
    url = "https://api.binance.com/api/v1/exchangeInfo"
    try:
        response = requests.get(url)
        list_trading_pairs = json.loads(response.text)
    except Exception as e:
        print(" Exception occured when trying to access " + url)
        print(e)
        return []

    symbols_list = []
    for pair in list_trading_pairs['symbols']:
        if pair['status'] == 'TRADING':
            symbols_list.append(pair['symbol'])
    return symbols_list

def getSymbolData(Ninjabot, symbol, interval):
    Ninjabot = Ninjabot
    # download data
    df = Ninjabot.klines(symbol=symbol, interval=interval)

    df = pd.DataFrame(df)
    df = df.drop(range(6, 12), axis=1)

    col_names = ['time', 'open', 'high', 'low', 'close', 'volume']
    df.columns = col_names

    for col in col_names:
        df[col] = df[col].astype(float)
    return df


def symbolfilter(pairs,Ninjabot):
    symbol_list = []
    # filtering by name
    for pair in pairs:
        ffs = pair[-4:]
        if 'USDT' == ffs:   
                symbol_list.append(pair)
    return symbol_list

def placeOrder(Ninjabot, symbol:str, side:str, type:str, quantity:float, price:float, test:bool):

    if test:
        try:
            data = Ninjabot.testOrder(
                symbol=symbol,
                recvWindow=5000,
                side=side,
                type=type,
                quantity=quantity,
                timestamp=int(round(time.time() * 1000))#?needed
            )
        except Exception as e:
            print(" Exception occured when trying to palce order on " + symbol)
            print(e)
            data = {'code': '-1', 'msg': e}
            return False
        print(data)
        return data

    else:
        try:

            #precision = 8
            #price_str = '{:0.0{}f}'.format(price, precision)

            data = Ninjabot.createOrder(
                symbol=symbol,
                recvWindow=5000,
                side=side,
                type=type,
                #timeInForce='GTC',
                quantity=quantity,
                #price=price_str,
                timestamp=int(round(time.time() * 1000))  # ?needed
            )
        except Exception as e:
            print(" Exception occured when trying to palce order on " + symbol)
            print(e)
            data = {'code': '-1', 'msg': e}
            return False
        print(data)
        return data

'''def cancelOrder(Ninjabot, ID, symbol):
    params = {
        'symbol': symbol,
        'orderId': ID,
        'recvWindow': 5000,
        'timestamp': int(round(time.time() * 1000))
    }
    try:
        canceldata = Ninjabot.cancelOrder(params)
        return canceldata["price"]
    except Exception as e:
        print(" Exception occured when trying to cancel order")
        print(e)
        canceldata = {'code': '-1', 'msg': e}
        return None'''
