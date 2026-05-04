from .base_strategy import BaseStrategy

class TrendFollowing(BaseStrategy):
    def __init__(self, kiwoom, universe, short_ma=5, long_ma=20):
        super().__init__(kiwoom)
        self.universe = universe
        self.short_ma = short_ma
        self.long_ma = long_ma

    def check_signal(self, code, df):
        """이동평균선 골든크로스 확인"""
        if len(df) < self.long_ma: return False
        
        ma_short = df['close'].rolling(window=self.short_ma).mean().iloc[-1]
        ma_long = df['close'].rolling(window=self.long_ma).mean().iloc[-1]
        ma_short_prev = df['close'].rolling(window=self.short_ma).mean().iloc[-2]
        ma_long_prev = df['close'].rolling(window=self.long_ma).mean().iloc[-2]
        
        if ma_short_prev <= ma_long_prev and ma_short > ma_long:
            print(f"📈 [TrendFollowing] {code} 골든크로스 발생!")
            return True
        return False
