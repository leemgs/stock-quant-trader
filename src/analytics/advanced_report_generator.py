import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from fpdf import FPDF
from datetime import datetime
from scipy import stats

class AdvancedReportGenerator:
    def __init__(self, db):
        self.df = db.get_all_trades()
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])

    def calculate_advanced_metrics(self):
        """논문 수준의 통계 지표 계산"""
        returns = self.df['profit'].pct_change().dropna()
        
        # 1. 샤프 지수 및 소르티노 지수
        sharpe = np.sqrt(252) * returns.mean() / returns.std() if returns.std() != 0 else 0
        downside_returns = returns[returns < 0]
        sortino = np.sqrt(252) * returns.mean() / downside_returns.std() if len(downside_returns) > 0 else 0
        
        # 2. 통계적 유의성 (T-test)
        # 귀무가설: 전략의 평균 수익은 0이다.
        t_stat, p_value = stats.ttest_1samp(returns, 0)
        
        # 3. MDD (최대 낙폭)
        cum_returns = (1 + returns).cumprod()
        peak = cum_returns.cummax()
        drawdown = (cum_returns - peak) / peak
        mdd = drawdown.min()
        
        return {
            "Sharpe Ratio": f"{sharpe:.2f}",
            "Sortino Ratio": f"{sortino:.2f}",
            "T-Statistic": f"{t_stat:.4f}",
            "P-Value": f"{p_value:.4f}",
            "Max Drawdown": f"{mdd*100:.2f}%",
            "Win Rate": f"{(returns > 0).mean()*100:.1f}%"
        }

    def generate_pdf(self, filename="reports/Advanced_Quant_Report.pdf"):
        metrics = self.calculate_advanced_metrics()
        
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        pdf.set_font("Arial", 'B', 20)
        pdf.cell(200, 20, "Quantitative Strategy Validation Report", ln=True, align='C')
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(200, 10, f"Issued Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='R')
        
        pdf.ln(10)
        
        # Section 1: Executive Summary
        pdf.set_font("Arial", 'B', 14)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(0, 10, "1. Performance Summary", ln=True, fill=True)
        pdf.set_font("Arial", '', 12)
        for k, v in metrics.items():
            pdf.cell(100, 10, f"{k}:", border=0)
            pdf.cell(100, 10, f"{v}", border=0, ln=True)
            
        pdf.ln(10)
        
        # Section 2: Statistical Significance
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "2. Statistical Validity Analysis", ln=True, fill=True)
        pdf.set_font("Arial", '', 11)
        validity_text = (
            f"The strategy demonstrates a P-Value of {metrics['P-Value']}. "
            f"At a 5% significance level, {'the results are statistically significant.' if float(metrics['P-Value']) < 0.05 else 'the results may be due to chance.'}"
        )
        pdf.multi_cell(0, 10, validity_text)
        
        # Section 3: Risk Assessment
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "3. Risk & Drawdown Assessment", ln=True, fill=True)
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(0, 10, f"The Maximum Drawdown (MDD) of {metrics['Max Drawdown']} indicates the peak-to-trough risk profile. "
                             f"The Sortino Ratio of {metrics['Sortino Ratio']} highlights the risk-adjusted return relative to downside volatility.")

        pdf.output(filename)
        print(f"✅ 논문 수준 리포트 생성 완료: {filename}")
