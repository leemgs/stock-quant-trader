import logging

class EnsembleEngine:
    def __init__(self, strategies):
        """
        strategies: { 'name': strategy_instance }
        weights: 각 전략별 투자 비중 (합계 1.0)
        """
        self.strategies = strategies
        self.weights = {name: 1.0/len(strategies) for name in strategies.keys()}
        self.performance = {name: 1.0 for name in strategies.keys()}

    def update_weights(self, strategy_performance):
        """성과에 따라 가중치 재조정 (Dynamic Allocation)"""
        # 성과가 좋은 전략에 더 많은 비중 할당 로직
        total_perf = sum(strategy_performance.values())
        if total_perf > 0:
            for name in self.weights:
                self.weights[name] = strategy_performance[name] / total_perf
        logging.info(f"전략 가중치 업데이트: {self.weights}")

    def get_signals(self, code, df):
        """모든 전략의 신호를 종합하여 최종 결정"""
        signals = {}
        for name, strategy in self.strategies.items():
            signals[name] = strategy.check_signal(code, df)
        
        # 가중치 투표 (Weighted Voting)
        final_score = sum(self.weights[name] for name, sig in signals.items() if sig)
        
        # 과반수 이상의 가중치가 찬성할 경우 매수 (임계값 0.5)
        if final_score >= 0.5:
            print(f"✅ [Ensemble] 종합 매수 신호 발생 (Score: {final_score:.2f})")
            return True
        return False
