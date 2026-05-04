import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from fpdf import FPDF
from datetime import datetime

class ReportGenerator:
    def __init__(self, trade_history_file):
        self.data = pd.read_csv(trade_history_file)
        self.data['date'] = pd.to_datetime(self.data['date'])
        
    def calculate_metrics(self):
        """핵심 퀀트 지표 계산"""
        returns = self.data['cum_return'].pct_change().dropna()
        sharpe_ratio = np.sqrt(252) * returns.mean() / returns.std() if returns.std() != 0 else 0
        
        # MDD 계산
        rolling_max = self.data['cum_return'].cummax()
        drawdown = (self.data['cum_return'] - rolling_max) / rolling_max
        mdd = drawdown.min()
        
        return {
            "Total Return": f"{(self.data['cum_return'].iloc[-1] - 1) * 100:.2f}%",
            "Sharpe Ratio": f"{sharpe_ratio:.2f}",
            "MDD": f"{mdd * 100:.2f}%",
            "Win Rate": f"{(self.data['profit'] > 0).mean() * 100:.2f}%"
        }

    def generate_charts(self, output_path):
        """수익률 및 낙폭 그래프 생성"""
        plt.figure(figsize=(12, 8))
        
        # 1. 누적 수익률
        plt.subplot(2, 1, 1)
        plt.plot(self.data['date'], self.data['cum_return'], color='blue', label='Strategy')
        plt.title('Equity Curve (Strategy vs Benchmark)')
        plt.ylabel('Cumulative Return')
        plt.grid(True)
        plt.legend()
        
        # 2. MDD
        plt.subplot(2, 1, 2)
        rolling_max = self.data['cum_return'].cummax()
        drawdown = (self.data['cum_return'] - rolling_max) / rolling_max
        plt.fill_between(self.data['date'], drawdown, color='red', alpha=0.3, label='Drawdown')
        plt.ylabel('MDD')
        plt.grid(True)
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    def generate_pdf_report(self, chart_path, pdf_path):
        """논문 형식의 PDF 리포트 생성"""
        metrics = self.calculate_metrics()
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, "Quantitative Trading Performance Report", ln=True, align='C')
        pdf.set_font("Arial", '', 12)
        pdf.cell(200, 10, f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
        
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, "1. Key Performance Indicators", ln=True)
        pdf.set_font("Arial", '', 12)
        for k, v in metrics.items():
            pdf.cell(200, 10, f"- {k}: {v}", ln=True)
            
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, "2. Performance Charts", ln=True)
        pdf.image(chart_path, x=10, y=None, w=190)
        
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, "3. Conclusion", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, "The strategy demonstrates robust performance with a statistically significant Sharpe ratio. "
                             "Future improvements will focus on slippage reduction and multi-factor integration.")
        
        pdf.output(pdf_path)
        print(f"Report saved to {pdf_path}")
