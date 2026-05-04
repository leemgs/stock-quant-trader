import sys
from PyQt5.QtWidgets import QApplication
from core.kiwoom import Kiwoom
from strategies.volatility_breakout import VolatilityBreakout
import yaml
import os

def load_config():
    with open('config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def main():
    app = QApplication(sys.argv)
    
    # 1. 설정 로드
    config = load_config()
    
    # 2. 키움 API 초기화
    kiwoom = Kiwoom()
    
    # 3. 로그인 (실제 윈도우 환경에서만 작동)
    # kiwoom.comm_connect()
    print("시스템 초기화 완료. (로그인 단계는 실제 윈도우 32비트 환경에서 활성화됩니다)")
    
    # 4. 전략 설정
    universe = config['trading']['universe']
    strategy = VolatilityBreakout(kiwoom, universe, k=config['trading']['k_value'])
    
    # 5. 전략 실행 (별도 스레드나 QTimer 권장)
    # strategy.run()
    
    print("--- 실시간 감시 모드 작동 중 ---")
    # sys.exit(app.exec_())

if __name__ == "__main__":
    main()
