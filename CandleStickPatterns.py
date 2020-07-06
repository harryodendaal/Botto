def observeBullishPinbar(df, i):
    candle_length = abs(df["open"][i] - df["close"][i])
    candle_body_low = min(df['open'][i], df['close'][i])
    candle_body_high = max(df['open'][i], df['close'][i])
    candle_stickbottom_length = candle_body_low - df['low'][i]
    candle_sticktop_length = df['high'][i] - candle_body_high

    if candle_stickbottom_length > 0:
        if candle_sticktop_length < 0.8 * candle_length and candle_length * 2 < candle_stickbottom_length:
            return True
    return False

def observeBearishPinbar(df, i):
    candle_length = abs(df["open"][i] - df["close"][i])
    candle_body_low = min(df['open'][i], df['close'][i])
    candle_body_high = max(df['open'][i], df['close'][i])
    candle_stickbottom_length = candle_body_low - df['low'][i]
    candle_sticktop_length = df['high'][i] - candle_body_high

    if candle_sticktop_length > 0:
        if candle_stickbottom_length < 0.8 * candle_length and candle_length * 2 < candle_sticktop_length:
            return True
    return False