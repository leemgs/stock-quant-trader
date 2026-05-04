import requests
import logging

class TelegramNotifier:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.enabled = True if token and chat_id else False

    def send_message(self, message):
        if not self.enabled:
            return

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {
            "chat_id": self.chat_id,
            "text": f"🚀 [Antigravity Trader]\n{message}",
            "parse_mode": "Markdown"
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                logging.error(f"Telegram 알림 전송 실패: {response.text}")
        except Exception as e:
            logging.error(f"Telegram 알림 에러: {str(e)}")

    def notify_order(self, code, type, qty, price):
        msg = (f"🔔 *주문 체결 알림*\n"
               f"- 종목: `{code}`\n"
               f"- 구분: {'🔴 매수' if type == 'BUY' else '🔵 매도'}\n"
               f"- 수량: {qty}주\n"
               f"- 단가: {price:,}원")
        self.send_message(msg)
