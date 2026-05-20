class CompoundManager:
    def __init__(self, initial_budget, target_profit_ratio=10.0):
        """
        initial_budget: 초기 자본 (예: 10,000원)
        target_profit_ratio: 목표 수익 배수 (예: 10배 = 100,000원)
        """
        self.current_equity = initial_budget
        self.target_equity = initial_budget * target_profit_ratio

    def update_equity(self, last_profit):
        """매매 결과에 따른 현재 자산 업데이트"""
        self.current_equity += last_profit
        print(f"💰 [Compound] 현재 자산: {self.current_equity:,.0f}원 (목표 대비 {self.get_progress():.1f}%)")

    def get_order_budget(self, risk_per_trade=0.2):
        """
        현재 자산의 일정 비율(예: 20%)을 한 종목에 투자
        소액일 경우 비중을 높여야 10배 달성이 가능함
        """
        if self.current_equity < 50000:
            return self.current_equity # 5만원 미만일 때는 전량 투입 (Aggressive)
        return self.current_equity * risk_per_trade

    def get_progress(self):
        """목표 달성률 반환"""
        return (self.current_equity / self.target_equity) * 100
