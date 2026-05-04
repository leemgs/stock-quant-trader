import pandas as pd

class SlippageAnalyzer:
    def __init__(self, theoretical_trades, actual_trades):
        """
        theoretical_trades: 백테스트상 체결 데이터
        actual_trades: 정밀 가상 매매 또는 실거래 데이터
        """
        self.theory = theoretical_trades
        self.actual = actual_trades

    def calculate_impact(self):
        """슬리피지가 전체 수익률에 미친 영향 계산"""
        theory_profit = self.theory['profit'].sum()
        actual_profit = self.actual['profit'].sum()
        
        slippage_cost = theory_profit - actual_profit
        impact_percent = (slippage_cost / theory_profit) * 100 if theory_profit != 0 else 0
        
        print(f"📊 [Slippage Analysis]")
        print(f"- 이론적 총 수익: {theory_profit:,.0f}원")
        print(f"- 실제 체결 수익: {actual_profit:,.0f}원")
        print(f"- 슬리피지 비용: {slippage_cost:,.0f}원")
        print(f"- 수익 감소율: {impact_percent:.2f}%")
        
        return impact_percent
