import pandas as pd
import matplotlib.pyplot as plt

class PerformanceComparer:
    def __init__(self, backtest_csv, real_trade_db):
        self.backtest_data = pd.read_csv(backtest_csv)
        self.real_data = real_trade_db.get_all_trades()

    def compare_returns(self, output_image):
        """백테스트 수익률과 실거래 수익률을 동일 차트에서 비교"""
        plt.figure(figsize=(10, 6))
        
        # 날짜별 누적 수익률 계산
        self.backtest_data['cum_return'].plot(label='Backtest (Theory)', color='gray', linestyle='--')
        
        if not self.real_data.empty:
            self.real_data['cum_return'] = (1 + self.real_data['profit'].pct_change()).cumprod()
            self.real_data['cum_return'].plot(label='Real Trading (Actual)', color='blue', linewidth=2)
        
        plt.title('Theory vs Reality: Performance Comparison')
        plt.xlabel('Trade Count / Date')
        plt.ylabel('Cumulative Return')
        plt.legend()
        plt.grid(True)
        plt.savefig(output_image)
        print(f"비교 분석 그래프가 {output_image}에 저장되었습니다.")

    def analyze_slippage(self):
        """이론가와 실제 체결가의 차이(슬리피지) 분석"""
        # 실거래 데이터의 평균 체결 오차 계산 로직
        pass
