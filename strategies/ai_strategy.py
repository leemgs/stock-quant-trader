import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from .base_strategy import BaseStrategy

class AIAlphaStrategy(BaseStrategy):
    def __init__(self, kiwoom, universe):
        super().__init__(kiwoom)
        self.model = RandomForestClassifier(n_estimators=100)
        self.universe = universe

    def prepare_features(self, df):
        """기술적 지표를 기반으로 학습용 데이터 생성"""
        df = df.copy()
        df['returns'] = df['close'].pct_change()
        df['ma5'] = df['close'].rolling(5).mean()
        df['ma20'] = df['close'].rolling(20).mean()
        df['vol_ma'] = df['volume'].rolling(5).mean()
        
        # 타겟: 내일 종가가 오늘보다 높으면 1, 아니면 0
        df['target'] = np.where(df['close'].shift(-1) > df['close'], 1, 0)
        return df.dropna()

    def train(self, training_data_dict):
        """복수 종목 데이터를 통합하여 모델 학습"""
        all_features = []
        for code, df in training_data_dict.items():
            processed = self.prepare_features(df)
            all_features.append(processed)
        
        train_df = pd.concat(all_features)
        X = train_df[['returns', 'ma5', 'ma20', 'vol_ma']]
        y = train_df['target']
        self.model.fit(X, y)
        print("AI 모델 학습 완료.")

    def check_signal(self, code, current_data):
        """현재 데이터를 입력받아 매수 시그널(확률) 예측"""
        # (간소화) 실거래 시에는 최근 N일 데이터를 feature로 변환하여 전달
        # X_current = [current_returns, current_ma5, ...]
        # prediction = self.model.predict(X_current)
        # return True if prediction == 1 else False
        return False

    def run(self):
        print("AI 실시간 감시 루프 가동...")
        # 실시간 데이터 수집 및 모델 예측 루프 구현
