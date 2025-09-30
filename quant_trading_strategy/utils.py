import pandas as pd

def calculate_sharpe(equity_series, k_per_day=78):
    returns = equity_series.pct_change().dropna()
    if returns.std() != 0:
        return returns.mean() / returns.std() * (k_per_day*252)**0.5
    return 0

def calculate_drawdown(equity_series):
    peak = equity_series.cummax()
    drawdown = equity_series - peak
    max_dd = abs(drawdown.min())
    max_dd_pct = max_dd / equity_series.iloc[0] * 100
    return max_dd, max_dd_pct

def calculate_profit_loss_ratio(trades):
    total_profit = sum(t['profit'] for t in trades if t['profit'] > 0)
    total_loss   = -sum(t['profit'] for t in trades if t['profit'] < 0)
    return total_profit / total_loss if total_loss != 0 else float('inf')

