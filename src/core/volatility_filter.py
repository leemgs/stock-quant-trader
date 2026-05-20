class VolatilityFilter:
    def __init__(self, min_volume_growth=5.0, min_volatility=0.03):
        """
        min_volume_growth: 전일 대비 거래량 증가율 (최소 5배)
        min_volatility: 최소 변동성 (최소 3% 이상 움직이는 종목)
        """
        self.min_volume_growth = min_volume_growth
        self.min_volatility = min_volatility

    def filter_candidates(self, market_data):
        """
        시장 데이터를 분석하여 '돈이 몰리는' 급등 후보주 선별
        market_data: [{code, volume_ratio, vol_index}, ...]
        """
        candidates = []
        for stock in market_data:
            if stock['volume_ratio'] >= self.min_volume_growth and stock['vol_index'] >= self.min_volatility:
                candidates.append(stock['code'])
        
        print(f"🔥 [VolatilityFilter] 급등 후보군 {len(candidates)}종목 포착")
        return candidates
