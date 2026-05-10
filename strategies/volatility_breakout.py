import time
from .base_strategy import BaseStrategy

class VolatilityBreakout(BaseStrategy):
    def __init__(self, broker, universe, k=0.5):
        super().__init__(broker)
        self.universe = universe
        self.k = k
        self.target_prices = {}
        
    def calculate_target_prices(self):
        """전일 데이터를 바탕으로 당일 목표가 계산"""
        for code in self.universe:
            # KIS API를 통한 전일 데이터 조회 로직 (샘플)
            # res = self.broker.api.fetch_ohlcv(code, timeframe='D', count=2)
            # prev_high = float(res['output2'][1]['stck_hgpr'])
            # prev_low = float(res['output2'][1]['stck_lwpr'])
            # curr_open = float(res['output2'][0]['stck_oprc'])
            
            # (샘플 가상 로직)
            prev_high = 10000
            prev_low = 9000
            curr_open = 9500
            
            target = curr_open + (prev_high - prev_low) * self.k
            self.target_prices[code] = target
            print(f"[{code}] 목표가: {self.target_prices[code]}")

    def check_signal(self, code, df):
        """실시간 가격이 목표가를 돌파했는지 확인"""
        if code not in self.target_prices:
            return False
            
        # df에서 현재가 추출 또는 broker에서 현재가 획득
        current_price = self.broker.get_price(code)
            
        if current_price >= self.target_prices[code]:
            return True
        return False

    def run(self):
        self.calculate_target_prices()
        print("Volatility Breakout 실시간 모니터링 시작...")
        
        while True:
            for code in self.universe:
                if self.check_signal(code, None):
                    print(f"🎯 [{code}] 변동성 돌파 발생! 매수")
                    # self.broker.send_order(code, 10, 0, "01")
                    self.universe.remove(code)
            
            time.sleep(1)
