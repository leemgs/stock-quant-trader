import yfinance as yf
import logging

class MacroCollector:
    def __init__(self):
        self.symbols = {
            "Nasdaq": "^IXIC",
            "S&P500": "^GSPC",
            "USD/KRW": "USDKRW=X"
        }

    def get_market_status(self):
        """글로벌 지수 및 환율의 전일 대비 등락폭 계산"""
        status = {}
        try:
            for name, symbol in self.symbols.items():
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="2d")
                if len(hist) >= 2:
                    prev_close = hist['Close'].iloc[-2]
                    curr_price = hist['Close'].iloc[-1]
                    change_pct = ((curr_price - prev_close) / prev_close) * 100
                    status[name] = change_pct
                else:
                    status[name] = 0.0
        except Exception as e:
            logging.error(f"거시지표 수집 에러: {str(e)}")
            return None
        return status
