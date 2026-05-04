import logging

class VirtualExchange:
    def __init__(self, initial_balance=10000000):
        self.balance = initial_balance
        self.holdings = {} # {code: {'qty': 0, 'avg_price': 0}}
        self.pending_orders = [] # [{'code': '', 'type': '', 'qty': 0, 'price': 0}]
        self.slippage_rate = 0.0005 # 기본 0.05% 슬리피지 적용

    def process_order_matching(self, code, current_bid_hoga, current_ask_hoga):
        """
        실시간 호가 데이터를 기반으로 미체결 주문 매칭
        current_bid_hoga: [(가격, 잔량), (가격, 잔량), ...]
        current_ask_hoga: [(가격, 잔량), (가격, 잔량), ...]
        """
        matched_indices = []
        for i, order in enumerate(self.pending_orders):
            if order['code'] != code: continue
            
            # 매수 주문 처리: 매도 호가(Ask)에 잔량이 있고 가격이 맞는지 확인
            if order['type'] == 'BUY':
                ask_price, ask_qty = current_ask_hoga[0] # 최우선 매도호가
                if order['price'] >= ask_price and ask_qty >= order['qty']:
                    self._execute_buy(order, ask_price)
                    matched_indices.append(i)
            
            # 매도 주문 처리: 매수 호가(Bid)에 잔량이 있고 가격이 맞는지 확인
            elif order['type'] == 'SELL':
                bid_price, bid_qty = current_bid_hoga[0] # 최우선 매수호가
                if order['price'] <= bid_price and bid_qty >= order['qty']:
                    self._execute_sell(order, bid_price)
                    matched_indices.append(i)
        
        # 체결된 주문 제거
        for i in sorted(matched_indices, reverse=True):
            self.pending_orders.pop(i)

    def _execute_buy(self, order, match_price):
        # 슬리피지 적용 (실제로는 가격이 조금 더 높게 체결됨)
        execution_price = match_price * (1 + self.slippage_rate)
        total_cost = execution_price * order['qty']
        
        if self.balance >= total_cost:
            self.balance -= total_cost
            code = order['code']
            current_holding = self.holdings.get(code, {'qty': 0, 'avg_price': 0})
            
            new_qty = current_holding['qty'] + order['qty']
            new_avg = (current_holding['qty'] * current_holding['avg_price'] + total_cost) / new_qty
            self.holdings[code] = {'qty': new_qty, 'avg_price': new_avg}
            logging.info(f"🟢 [V-Trade] 매수 체결: {code}, {order['qty']}주 @ {execution_price:,.0f}원")

    def _execute_sell(self, order, match_price):
        execution_price = match_price * (1 - self.slippage_rate)
        revenue = execution_price * order['qty']
        
        code = order['code']
        if code in self.holdings and self.holdings[code]['qty'] >= order['qty']:
            self.balance += revenue
            self.holdings[code]['qty'] -= order['qty']
            profit = (execution_price - self.holdings[code]['avg_price']) * order['qty']
            logging.info(f"🔴 [V-Trade] 매도 체결: {code}, {order['qty']}주 @ {execution_price:,.0f}원 (손익: {profit:,.0f})")
            if self.holdings[code]['qty'] == 0:
                del self.holdings[code]
