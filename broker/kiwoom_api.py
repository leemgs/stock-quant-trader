
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop

class KiwoomAPI(QAxWidget):
    def __init__(self):
        super().__init__()
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
        self.login_event_loop = QEventLoop()

        self.OnEventConnect.connect(self._on_login)

    def login(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop.exec_()

    def _on_login(self, err_code):
        if err_code == 0:
            print("로그인 성공")
        else:
            print("로그인 실패")
        self.login_event_loop.exit()

    def send_order(self, code, qty, price, order_type):
        print(f"주문: {code}, {qty}, {price}, {order_type}")
