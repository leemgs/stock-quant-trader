import sys
import time
from PyQt5.QtWidgets import QApplication
from datetime import datetime
from core.kiwoom import Kiwoom
from core.ensemble_engine import EnsembleEngine
from core.notifier import TelegramNotifier
from core.database import TradeDatabase
from core.risk_manager import MarketRiskManager
from core.macro_collector import MacroCollector
from strategies.volatility_breakout import VolatilityBreakout
from strategies.mean_reversion import MeanReversion
from strategies.trend_following import TrendFollowing
import yaml

def load_config():
    with open('config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def main():
    app = QApplication(sys.argv)
    config = load_config()
    
    # 1. 시스템 초기화
    print("🚀 Antigravity Quant Trader 시스템 시동 중...")
    db = TradeDatabase()
    notifier = TelegramNotifier(config['auth']['telegram_token'], config['auth']['chat_id'])
    kiwoom = Kiwoom()
    
    # 2. 로그인
    kiwoom.comm_connect()
    print("✅ 로그인 성공 및 계좌 정보 확인 완료")
    
    # 3. 전략 앙상블 구성
    universe = config['trading']['universe']
    strategies = {
        "Breakout": VolatilityBreakout(kiwoom, universe),
        "MeanReversion": MeanReversion(kiwoom, universe),
        "TrendFollowing": TrendFollowing(kiwoom, universe)
    }
    ensemble = EnsembleEngine(strategies)
    
    # 4. 리스크 매니저 초기화 (투자 한도 설정 포함)
    risk_manager = MarketRiskManager(MacroCollector(), max_budget=config['trading']['max_budget'])
    
    # 5. 자동매매 메인 루프
    print("🔍 실시간 시장 감시 모드 진입")
    notifier.send_message("자동매매 시스템이 시작되었습니다.")
    
    while True:
        now = datetime.now()
        # 장중 시간 확인 (09:00 ~ 15:20)
        if now.hour >= 9 and (now.hour < 15 or (now.hour == 15 and now.minute <= 20)):
            # 글로벌 리스크 확인 (세이프 가드)
            multiplier = risk_manager.get_trading_multiplier()
            
            if multiplier > 0:
                for code in universe:
                    # 앙상블 신호 확인 (돌파+평균회귀+추세추종 종합)
                    # 실제 구현 시에는 df(분봉/일봉 데이터) 수집 로직 필요
                    df = pd.DataFrame() # 데이터 수집 로직 대체
                    if ensemble.get_signals(code, df):
                        print(f"🎯 [{code}] 매수 조건 충족! 주문 집행 (비중: {multiplier})")
                        # kiwoom.send_order(...)
                        # db.log_trade(...)
                        # notifier.notify_order(...)
            else:
                print("⚠️ 글로벌 리스크 과다로 매매 일시 정지 (Safe Guard Active)")
        else:
            if now.hour == 15 and now.minute > 30:
                print("💤 장 종료. 시스템을 대기 모드로 전환합니다.")
                time.sleep(3600) # 1시간 대기
        
        time.sleep(1) # 1초 간격 루프

if __name__ == "__main__":
    main()
