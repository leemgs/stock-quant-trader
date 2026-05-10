import sys
import time
from datetime import datetime
import pandas as pd
import yaml
import logging

from broker.kis_api import KISBroker
from core.ensemble_engine import EnsembleEngine
from core.notifier import TelegramNotifier
from core.database import TradeDatabase
from core.risk_manager import MarketRiskManager
from core.macro_collector import MacroCollector
from strategies.volatility_breakout import VolatilityBreakout
from strategies.mean_reversion import MeanReversion
from strategies.trend_following import TrendFollowing

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/trading.log"),
        logging.StreamHandler()
    ]
)

def load_config():
    with open('config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def main():
    config = load_config()
    
    # 1. 시스템 초기화
    print("🚀 Antigravity Quant Trader (KIS Edition) 시스템 시동 중...")
    db = TradeDatabase()
    notifier = TelegramNotifier(config['auth']['telegram_token'], config['auth']['chat_id'])
    
    # 2. KIS API 브로커 초기화 (Ubuntu 호환)
    broker = KISBroker(config)
    print("✅ KIS API 연결 및 계좌 정보 확인 완료")
    
    # 3. 전략 앙상블 구성
    universe = config['trading']['universe']
    strategies = {
        "Breakout": VolatilityBreakout(broker, universe),
        "MeanReversion": MeanReversion(broker, universe),
        "TrendFollowing": TrendFollowing(broker, universe)
    }
    ensemble = EnsembleEngine(strategies)
    
    # 4. 리스크 매니저 초기화
    risk_manager = MarketRiskManager(MacroCollector(), max_budget=config['trading']['max_budget'])
    
    # 5. 자동매매 메인 루프
    print("🔍 실시간 시장 감시 모드 진입 (Ubuntu Environment)")
    notifier.send_message("KIS 자동매매 시스템이 시작되었습니다.")
    
    try:
        while True:
            now = datetime.now()
            # 장중 시간 확인 (09:00 ~ 15:20)
            if now.hour >= 9 and (now.hour < 15 or (now.hour == 15 and now.minute <= 20)):
                # 글로벌 리스크 확인
                multiplier = risk_manager.get_trading_multiplier()
                
                if multiplier > 0:
                    for code in universe:
                        # 현재가 및 데이터 수집 (실제 구현 시 KIS API 활용 데이터프레임 생성 필요)
                        price = broker.get_price(code)
                        df = pd.DataFrame() # 데이터 수집 로직 (샘플)
                        
                        if ensemble.get_signals(code, df):
                            print(f"🎯 [{code}] 매수 조건 충족! 현재가: {price}")
                            # 주문 집행
                            # qty = int((config['trading']['max_budget'] * multiplier) / price)
                            # broker.send_order(code, qty, price, order_type="01")
                            # db.log_trade(...)
                            # notifier.notify_order(...)
                else:
                    logging.warning("⚠️ 글로벌 리스크 과다로 매매 일시 정지")
            else:
                if now.hour == 15 and now.minute > 30:
                    print("💤 장 종료. 시스템을 대기 모드로 전환합니다.")
                    time.sleep(3600)
            
            time.sleep(10) # API 호출 제한을 고려하여 주기 조정
    except KeyboardInterrupt:
        print("\n🛑 사용자에 의해 시스템이 중단되었습니다.")
    except Exception as e:
        logging.error(f"❌ 예기치 못한 오류 발생: {e}")
        notifier.send_message(f"🚨 시스템 오류 발생: {e}")

if __name__ == "__main__":
    main()
