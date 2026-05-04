import pandas as pd
import numpy as np

class BacktestEngine:
    def __init__(self, initial_budget=10000000, commission=0.00015):
        self.budget = initial_budget
        self.commission = commission
        self.holdings = {}
        self.history = []

    def run(self, strategy, data_dict):
        """
        data_dict: { 'code': pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume']) }
        """
        print("백테스트 시뮬레이션 시작...")
        
        # 날짜별 루프 (모든 종목의 날짜를 정렬하여 진행)
        all_dates = sorted(pd.concat(data_dict.values())['date'].unique())
        
        for date in all_dates:
            for code, df in data_dict.items():
                day_data = df[df['date'] == date]
                if day_data.empty: continue
                
                row = day_data.iloc[0]
                current_price = row['close']
                
                # 1. 매수 시그널 체크
                if code not in self.holdings and strategy.check_signal(code, row):
                    quantity = (self.budget * 0.1) // current_price
                    if quantity > 0:
                        cost = quantity * current_price * (1 + self.commission)
                        self.budget -= cost
                        self.holdings[code] = {'quantity': quantity, 'buy_price': current_price}
                        self.history.append({'date': date, 'type': 'BUY', 'code': code, 'price': current_price, 'profit': 0})

                # 2. 매도 시그널 체크 (예: 장마감 전량 매도 전략)
                elif code in self.holdings:
                    # 수익률 기반 매도 시그널 예시 (간소화)
                    if True: # 전략에 따른 조건 추가
                        qty = self.holdings[code]['quantity']
                        revenue = qty * current_price * (1 - self.commission)
                        profit = revenue - (qty * self.holdings[code]['buy_price'])
                        self.budget += revenue
                        del self.holdings[code]
                        self.history.append({'date': date, 'type': 'SELL', 'code': code, 'price': current_price, 'profit': profit})

        return pd.DataFrame(self.history)
