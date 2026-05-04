import sys
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop
import logging

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
        self.login_event_loop = QEventLoop()
        
        # API Event Slots
        self.OnEventConnect.connect(self._handler_login)
        self.OnReceiveTrData.connect(self._handler_tr_data)
        self.OnReceiveMsg.connect(self._handler_msg)
        self.OnReceiveRealData.connect(self._handler_real_data)
        self.OnReceiveChejanData.connect(self._handler_chejan_data)
        
        self.tr_data = {}
        self.tr_event_loop = QEventLoop()

    def comm_connect(self):
        """로그인 시도"""
        self.dynamicCall("CommConnect()")
        self.login_event_loop.exec_()

    def _handler_login(self, err_code):
        if err_code == 0:
            print("로그인 성공")
        else:
            print(f"로그인 실패: {err_code}")
        self.login_event_loop.exit()

    def get_login_info(self, tag):
        """사용자 정보 획득 (ACCOUNT_CNT, ACCLIST, USER_ID 등)"""
        return self.dynamicCall("GetLoginInfo(QString)", tag)

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, trcode, next, screen_no)
        self.tr_event_loop.exec_()

    def _handler_tr_data(self, screen_no, rqname, trcode, record_name, next, *args):
        """TR 데이터 수신 핸들러"""
        self.tr_data[rqname] = {"trcode": trcode, "next": next}
        self.tr_event_loop.exit()

    def get_comm_data(self, trcode, record_name, index, item_name):
        ret = self.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, record_name, index, item_name)
        return ret.strip()

    def send_order(self, rqname, screen_no, acc_no, order_type, code, quantity, price, hoga_type, origin_order_no):
        """주문 전송"""
        return self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                                [rqname, screen_no, acc_no, order_type, code, quantity, price, hoga_type, origin_order_no])

    def _handler_msg(self, screen_no, rqname, trcode, msg):
        logging.info(f"[API MSG] Screen: {screen_no}, RQ: {rqname}, TR: {trcode}, Msg: {msg}")

    def _handler_real_data(self, code, real_type, real_data):
        # 실시간 데이터 수신 시 전략 엔진으로 토스하는 로직 필요
        pass

    def _handler_chejan_data(self, gubun, item_cnt, fid_list):
        """체결/잔고 수신 핸들러"""
        logging.info(f"[CHEJAN] Gubun: {gubun}")
