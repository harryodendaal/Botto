import CandleStickPatterns

class Indicatorstates:
    def __init__(self, _interval, _df, _icurrent):
        self.interval = _interval
        self.df = _df
        self.icurrent = _icurrent # make changeble
##########################---USING---####################################
    def rsiOverSold(self):
        if(self.df["rsi"][self.icurrent] < 60):
            return True
        else:
            return False
########################################################################







    def rsiOverBought(self):
        if(self.df["rsi"][self.icurrent] > 70):
            return True
        else:
             return False





##########################---USING---####################################
    def stochasticBuyCross(self):
        if self.df['fast'][self.icurrent] > self.df["slow"][self.icurrent]:
            return True
        else:
             return False
##########################################################################






    def stochasticSellCross(self):
        if self.df['fast'][self.icurrent] < self.df["slow"][self.icurrent]:
            return True
        else:
             return False





##########################---USING---####################################
    def stochasticOverSold(self):
        if self.df['fast'][self.icurrent] < 0.2 and self.df['slow'][self.icurrent] < 0.2:
            return True
        else:
             return False
    def stochasticOverBought(self):
        if self.df['fast'][self.icurrent] > 0.8 and self.df['slow'][self.icurrent] > 0.8:
            return True
        else:
             return False
    def pinbarBuySignal(self):
        return CandleStickPatterns.observeBullishPinbar(df=self.df, i=self.icurrent-1)
#########################################################################







    def pinbarSellSignal(self):
        return CandleStickPatterns.observeBearishPinbar(df=self.df, i=self.icurrent-1)

    def inCloud(self):
        self.icurrent = self.icurrent - 52
        upper_chikou_cloud = max(self.df['senkou_a'][self.icurrent], self.df['senkou_b'][self.icurrent])
        lower_chikou_cloud = min(self.df['senkou_a'][self.icurrent], self.df['senkou_b'][self.icurrent])
        if self.df['close'][self.icurrent] > lower_chikou_cloud and self.df['close'][self.icurrent] < upper_chikou_cloud:
            return True
        else:
             return False
    def aboveCloud(self):
        self.icurrent = self.icurrent - 52
        upper_chikou_cloud = max(self.df['senkou_a'][self.icurrent], self.df['senkou_b'][self.icurrent])
        if self.df['close'][self.icurrent] > upper_chikou_cloud:
            return True
        else:
            return False

    def belowCloud(self):
        self.icurrent = self.icurrent - 52
        lower_chikou_cloud = min(self.df['senkou_a'][self.icurrent], self.df['senkou_b'][self.icurrent])
        if self.df['close'][self.icurrent] > lower_chikou_cloud:
            return True
        else:
            return False

    def bollingerOverBought(self):
        if self.df['close'][self.icurrent] > self.df["upper_boll"][self.icurrent] or self.df['close'][self.icurrent - 1] > self.df['upper_boll'][self.icurrent - 1]:
            return True
        else:
             return False




##########################---USING---####################################
    def bollingerOverSold(self):
        if self.df['close'][self.icurrent] < self.df["low_boll"][self.icurrent] or self.df['close'][self.icurrent - 1] < self.df['low_boll'][self.icurrent - 1]:
            return True
        else:
             return False
#############################################################################





    def strategyState(self, strategy):
        if strategy == "beast":
            if self.bollingerOverSold() and self.stochasticBuyCross() and self.stochasticOverSold() and self.pinbarBuySignal():
                return True

        if strategy == "rsi":
            if self.rsiOverSold():
                return True
        return False
