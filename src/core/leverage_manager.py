import math

class DynamicLeverageManager:
    def __init__(self, initial_capital, max_margin_rate=2.5):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.max_margin_rate = max_margin_rate # 최대 미수/신용 레버리지 배수
        
        # 켈리 베팅을 위한 추적 데이터
        self.win_count = 0
        self.loss_count = 0
        self.total_win_rate = 0.0
        self.average_win_profit = 0.0
        self.average_loss_profit = 0.0
        
        self.trades = []

    def update_trade_result(self, is_win, profit_pct):
        """매매 결과 업데이트 (켈리 공식 계산용)"""
        self.trades.append((is_win, profit_pct))
        if is_win:
            self.win_count += 1
            # 간소화된 평균 수익률 계산
            self.average_win_profit = (self.average_win_profit * (self.win_count - 1) + profit_pct) / self.win_count
        else:
            self.loss_count += 1
            self.average_loss_profit = (self.average_loss_profit * (self.loss_count - 1) + abs(profit_pct)) / self.loss_count

        total_trades = self.win_count + self.loss_count
        self.total_win_rate = self.win_count / total_trades if total_trades > 0 else 0.0

    def calculate_kelly_fraction(self):
        """켈리 베팅 비율 계산 (최적 투자 비중)"""
        # f* = W - ((1 - W) / R)
        # W: 승률, R: 손익비 (평균수익/평균손실)
        if self.win_count + self.loss_count < 5:
            # 초기 데이터가 부족할 때는 보수적으로 50%만 베팅 (레버리지 없이)
            return 0.5 
            
        if self.average_loss_profit == 0:
            return 1.0 # 손실이 없으면 풀베팅
            
        reward_risk_ratio = self.average_win_profit / self.average_loss_profit
        if reward_risk_ratio == 0:
            return 0.0
            
        kelly_fraction = self.total_win_rate - ((1 - self.total_win_rate) / reward_risk_ratio)
        
        # 하프 켈리 (안정성을 위해 켈리 비율의 절반만 사용)
        half_kelly = kelly_fraction / 2.0
        
        # 비중은 0% ~ 100% 사이로 제한
        return max(0.0, min(1.0, half_kelly))

    def get_optimal_budget(self, current_account_balance, use_margin=True):
        """현재 잔고와 켈리 비율을 기반으로 최적의 투입 자본 계산 (레버리지 포함)"""
        kelly_ratio = self.calculate_kelly_fraction()
        
        # 기본 투입 자본
        base_budget = current_account_balance * kelly_ratio
        
        # 극단적 성장 모드 (미수/신용 풀레버리지)
        if use_margin and kelly_ratio > 0.3: # 승률/손익비가 좋을 때만 미수 사용
            # 보유 자금의 최대 max_margin_rate 배수까지 미수 풀베팅
            optimal_budget = base_budget * self.max_margin_rate
            return optimal_budget
            
        return base_budget

    def enforce_margin_liquidation(self, current_time):
        """15:15 즈음 미수 동결 방지를 위한 강제 청산 신호 (오버나잇 예외 제외)"""
        # "15:15:00" 이후인지 확인
        if current_time >= "15:15:00":
            return True
        return False
