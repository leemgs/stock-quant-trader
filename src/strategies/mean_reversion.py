import pandas as pd
from .base_strategy import BaseStrategy

class MeanReversion(BaseStrategy):
    def __init__(self, broker, universe, rsi_period=14, buy_threshold=30):
        super().__init__(broker)
        self.universe = universe
        self.rsi_period = rsi_period
        self.buy_threshold = buy_threshold

    def calculate_rsi(self, prices):
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
        rs = gain / loss
        return 100 - (100 / (1+rs))

    def check_signal(self, code, df):
        """RSI 지표를 활용한 과매도 구간 매수 신호 포착"""
        if len(df) < self.rsi_period + 1: return False
        
        rsi = self.calculate_rsi(df['close']).iloc[-1]
        if rsi <= self.buy_threshold:
            print(f"📉 [MeanReversion] {code} 과매도 포착 (RSI: {rsi:.1f})")
            return True
        return False
