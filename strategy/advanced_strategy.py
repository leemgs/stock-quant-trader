
import pandas as pd

class AdvancedStrategy:
    def market_filter(self, prices):
        ma = prices.rolling(200).mean()
        return prices.iloc[-1] > ma.iloc[-1]

    def entry(self, prices):
        ma = prices.rolling(20).mean()
        std = prices.rolling(20).std()
        return prices.iloc[-1] < (ma - 2*std).iloc[-1]
