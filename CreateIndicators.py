from pyti.relative_strength_index import relative_strength_index
from pyti.simple_moving_average import simple_moving_average
from pyti.exponential_moving_average import exponential_moving_average
from pyti.bollinger_bands import lower_bollinger_band as lbb
from pyti.bollinger_bands import upper_bollinger_band as ubb


def createRsi(symbol, df):
    try:
        df['rsi'] = relative_strength_index(df['close'].tolist(), 14)
        return df
    except Exception as e:
        print(" Exception raised when trying to compute rsi on " + symbol)
        print(e)
        return None

def createBands(symbol, df):
    try:
        df['low_boll'] = lbb(df['close'].tolist(), 14)
        df['upper_boll'] = ubb(df['close'].tolist(), 14)

        return df
    except Exception as e:
        print(" Exception raised when trying to compute bollingers on " + symbol)
        print(e)
        return None

def createEma(symbol, df):
    try:
        df['21 EMA'] = exponential_moving_average(df['close'].tolist(), 12)
        # df['26 EMA'] = exponential_moving_average(df['close'].tolist(), 26)

        return df
    except Exception as e:
        print(" Exception raised when trying to compute ema's on " + symbol)
        print(e)
        return None


def createIchimokuCloud(symbol, df):

    try:
        for col in df.columns:
            if col != "senkou a" and col != "senkou b" and col != 'time':
                df[col] = df[col].shift(-26)
        # Tenkan-sen (Conversion Line): (9-period hign + 9-period low)/2
        nine_period_high = df['high'].rolling(window=9).max()
        nine_period_low = df['low'].rolling(window=9).min()
        df['tenkansen'] = (nine_period_high + nine_period_low)/2

        # Kijun-sen (Base Line): (26-period high + 26-period low)/2
        period26_high = df['high'].rolling(window=26).max()
        period26_low = df['low'].rolling(window=26).min()
        df['kijunsen'] = (period26_high + period26_low)/2

        # Senkou Span A (Leading Span A): (Conversion Line + Base Line)/2
        df['senkou_a'] = ((df['tenkansen'] + df['kijunsen']) / 2 ).shift(26)

        # Senkou Span B
        period52_high = df['high'].rolling(window=52).max()
        period52_low = df['low'].rolling(window=52).min()
        df['senkou_b'] = ((period52_high + period52_low) / 2).shift(26)  #changed to 26

        # Chikou Span: Most recent closing price, plotted 26 periods behind (optional)
        df['chikouspan'] = df['close'].shift(-26)

        return df

    except Exception as e:
        print(" Exception raised when trying to compute ichimoku on " + symbol)
        print(e)
        return None
def createStochOscillator(symbol, df):

    try:
        period14_high = df['high'].rolling(window=14).max()
        period14_low = df['low'].rolling(window=14).min()
        df['slow'] = (df['close'] - period14_low)/(period14_high - period14_low)
        df['fast'] = simple_moving_average(df['slow'], 3)
        #smoothing 3 for some reasson
        df['slow'] = simple_moving_average(df['slow'], 3)
        df['fast'] = simple_moving_average(df['fast'], 3)
        return df

    except Exception as e:
        print(" Exception raised when trying to compute stockOscillator on " + symbol)
        print(e)
        return None


class CreatIndicators:
    INDICATORS_DICT = {
        "rsi": createRsi,
        "ema": createEma,
        "bb": createBands,
        'stochastic': createStochOscillator,
        "ichimoku": createIchimokuCloud,
    }
def createIndicators(df, symbol, indicator_name):
    if "rsi" in indicator_name:
        df = CreatIndicators.INDICATORS_DICT["rsi"](symbol=symbol, df=df)

    if "ema" in indicator_name:
        df = CreatIndicators.INDICATORS_DICT["ema"](symbol=symbol, df=df)

    if "bb"  in indicator_name:
        df = CreatIndicators.INDICATORS_DICT["bb"](symbol=symbol, df=df)

    if "stochastic" in indicator_name:
        df = CreatIndicators.INDICATORS_DICT["stochastic"](symbol=symbol, df=df)

    if "ichimoku" in indicator_name:
        df = CreatIndicators.INDICATORS_DICT["ichimoku"](symbol=symbol, df=df)

    return df