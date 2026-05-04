
import sys
from PyQt5.QtWidgets import QApplication
from broker.kiwoom_api import KiwoomAPI
from strategy.advanced_strategy import AdvancedStrategy

class Trader:
    def __init__(self):
        self.api = KiwoomAPI()
        self.strategy = AdvancedStrategy()

    def start(self):
        self.api.login()
        print("로그인 완료 대기...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    trader = Trader()
    trader.start()
    sys.exit(app.exec_())
