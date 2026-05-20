import time
from .base_strategy import BaseStrategy
from core.news_analyzer import NewsSentimentAnalyzer

class NewsSentimentStrategy(BaseStrategy):
    def __init__(self, broker, universe, gemini_api_key, threshold=70):
        super().__init__(broker)
        self.universe = universe
        self.analyzer = NewsSentimentAnalyzer(gemini_api_key)
        self.threshold = threshold

    def check_signal(self, code):
        """실시간 뉴스를 분석하여 매수 신호 확인"""
        titles = self.analyzer.get_latest_news(code)
        if not titles:
            return False

        sentiment_score = self.analyzer.analyze_sentiment(titles)
        print(f"[{code}] 뉴스 감성 점수: {sentiment_score}")

        if sentiment_score >= self.threshold:
            print(f"🔥 [{code}] 호재 발생! (점수: {sentiment_score}) 매수 진입 검토")
            return True
        return False

    def run(self):
        print("📰 [뉴스 감성 분석 모듈] 상시 감시 중...")
        while True:
            for code in self.universe:
                if self.check_signal(code):
                    # 실거래 주문 로직 연동
                    # self.broker.send_order(...)
                    pass
                time.sleep(2) # API 과부하 방지
