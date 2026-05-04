import time
from .base_strategy import BaseStrategy

class VolatilityBreakout(BaseStrategy):
    def __init__(self, kiwoom, universe, k=0.5):
        super().__init__(kiwoom)
        self.universe = universe
        self.k = k
        self.target_prices = {}
        
    def calculate_target_prices(self):
        """전일 데이터를 바탕으로 당일 목표가 계산"""
        for code in self.universe:
            # TR 요청 (opt10001: 주식기본정보요청) - 실제 구현 시에는 전일 고가/저가 필요
            # 여기서는 예시로 로직의 흐름만 구현
            # self.kiwoom.set_input_value("종목코드", code)
            # self.kiwoom.comm_rq_data("target_price_rq", "opt10001", 0, "0101")
            
            # (가정) 전일 고가: 10000, 전일 저가: 9000, 금일 시가: 9500
            # target = 9500 + (10000 - 9000) * 0.5 = 10000
            self.target_prices[code] = 10000 # 실시간 계산 로직 필요
            print(f"[{code}] 목표가: {self.target_prices[code]}")

    def check_signal(self, code, current_price):
        """실시간 가격이 목표가를 돌파했는지 확인"""
        if code not in self.target_prices:
            return False
            
        if current_price >= self.target_prices[code]:
            return True
        return False

    def run(self):
        self.calculate_target_prices()
        print("실시간 매매 루프 시작...")
        
        while True:
            # 장중(09:00 ~ 15:20) 루프
            for code in self.universe:
                # 1. 현재가 획득 (실제로는 API 실시간 데이터 핸들러에서 처리 권장)
                current_price = 10500 # 예시값
                
                if self.check_signal(code, current_price):
                    print(f"[{code}] 시그널 발생! 매수 주문 전송")
                    # self.kiwoom.send_order("buy_order", "0101", "계좌번호", 1, code, 10, 0, "03", "")
                    # 주문 후 유니버스에서 제거하여 중복 매수 방지
                    self.universe.remove(code)
            
            time.sleep(1)
            # 15:20 이후 루프 종료 및 전량 매도 로직 추가 필요
