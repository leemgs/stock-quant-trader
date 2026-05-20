from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    def __init__(self, broker):
        self.broker = broker
        self.universe = [] # 매매 대상 종목

    @abstractmethod
    def run(self):
        """전략 실행 메인 루프"""
        pass

    @abstractmethod
    def check_signal(self, code, df):
        """매수/매도 시그널 확인"""
        pass
