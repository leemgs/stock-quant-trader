# Trading Methodology & Technical Whitepaper

## 1. Mathematical Modeling of Volatility Breakout
The core strategy utilizes the concept of **Price Momentum** and **Volatility Expansion**. 
The target entry price $P_{target}$ is defined as:
$$P_{target} = P_{open} + (H_{prev} - L_{prev}) \times K$$
where:
- $P_{open}$: Current day's opening price
- $H_{prev}$: Previous day's high
- $L_{prev}$: Previous day's low
- $K$: Sensitivity coefficient (Range: 0.4 to 0.6)

## 2. Risk Management Framework
To ensure capital preservation, the system implements a **Fixed Fractional Position Sizing** model. 
The number of shares $N$ is calculated as:
$$N = \frac{Equity \times RiskPerTrade}{ATR \times Multiplier}$$
This ensures that no single trade can cause a catastrophic loss to the portfolio.

## 3. Performance Metrics for Validation
The system evaluates performance using the following academic metrics:
- **Sharpe Ratio**: Risk-adjusted return measure.
- **Max Drawdown (MDD)**: The maximum observed loss from a peak to a trough.
- **Profit Factor**: Gross profit divided by gross loss.
- **P-Value (Strategy Significance)**: To ensure the strategy performance is not due to random chance.

## 4. AI/ML Integration Pipeline
The framework supports ensemble learning methods. Feature importance analysis is performed to select the most predictive technical indicators, reducing overfitting (Variance) while maintaining low Bias.
