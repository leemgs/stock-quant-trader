
import pandas as pd
import numpy as np

def compute_metrics(df):
    returns = df['returns']
    cumulative = (1 + returns).cumprod()

    sharpe = returns.mean() / returns.std() * np.sqrt(252)
    mdd = (cumulative / cumulative.cummax() - 1).min()
    win_rate = (returns > 0).mean()

    return {
        "sharpe": sharpe,
        "mdd": mdd,
        "win_rate": win_rate,
        "total_return": cumulative.iloc[-1] - 1
    }

def generate_report(df):
    metrics = compute_metrics(df)

    report = f"""
# Quant Strategy Report

## Performance Metrics
- Sharpe Ratio: {metrics['sharpe']:.2f}
- Max Drawdown: {metrics['mdd']:.2%}
- Win Rate: {metrics['win_rate']:.2%}
- Total Return: {metrics['total_return']:.2%}

## Conclusion
Strategy shows {'positive' if metrics['sharpe'] > 1 else 'weak'} risk-adjusted return.
"""

    with open("report.md", "w", encoding="utf-8") as f:
        f.write(report)

    print("Report generated: report.md")

if __name__ == "__main__":
    # dummy test data
    np.random.seed(0)
    returns = np.random.normal(0.001, 0.02, 252)
    df = pd.DataFrame({"returns": returns})
    generate_report(df)
