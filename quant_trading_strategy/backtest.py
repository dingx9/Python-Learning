import pandas as pd

def backtest_strategy(df, ma_short=60, ma_long=120, stop_loss_usd=350,
                      initial_capital=50000, max_lots=3, risk_per_trade=2000,
                      point_value=20):
    df = df.copy()
    # ====== 技術指標 ======
    df['MA_short'] = df['Close'].rolling(window=ma_short).mean()
    df['MA_long']  = df['Close'].rolling(window=ma_long).mean()

    short_ema = df['Close'].ewm(span=12, adjust=False).mean()
    long_ema  = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = short_ema - long_ema
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # ====== 回測邏輯 ======
    trades = []
    equity_curve = []
    position = None
    entry_price, entry_lots, entry_time = 0, 0, None
    capital = 0

    for i in range(ma_long, len(df)):
        price = df['Close'].iloc[i]

        # 買入條件 (簡化版，放你原本邏輯)
        if position is None and df['MA_short'].iloc[i] > df['MA_long'].iloc[i]:
            allowed_lots = risk_per_trade / stop_loss_usd
            entry_lots = max(1, min(max_lots, int(allowed_lots)))
            position = 1
            entry_price = price
            entry_time = df.index[i]

        # 賣出條件
        elif position == 1 and (df['MA_short'].iloc[i] < df['MA_long'].iloc[i] or 
                                price <= entry_price - stop_loss_usd/point_value):
            profit_points = price - entry_price
            profit_usd = profit_points * point_value * entry_lots
            trades.append({
                "entry_time": entry_time,
                "entry_price": entry_price,
                "exit_time": df.index[i],
                "exit_price": price,
                "profit": profit_usd,
                "lots": entry_lots
            })
            capital += profit_usd
            position = None

        current_equity = initial_capital + capital + (
            (price - entry_price) * point_value * entry_lots if position else 0
        )
        equity_curve.append(current_equity)

    equity_series = pd.Series(equity_curve, index=df.index[-len(equity_curve):])

    # ====== 績效指標 ======
    total_trades = len(trades)
    total_profit = sum(t['profit'] for t in trades if t['profit'] > 0)
    total_loss   = -sum(t['profit'] for t in trades if t['profit'] < 0)
    win_rate     = sum(1 for t in trades if t['profit'] > 0) / total_trades * 100 if total_trades > 0 else 0
    max_loss     = min((t['profit'] for t in trades), default=0)

    peak = equity_series.cummax()
    drawdown = equity_series - peak
    max_drawdown = abs(drawdown.min())
    max_drawdown_pct = max_drawdown / initial_capital * 100

    profit_loss_ratio = total_profit / total_loss if total_loss > 0 else float('inf')
    returns = equity_series.pct_change().dropna()
    sharpe_ratio = returns.mean() / returns.std() * (78*252)**0.5 if returns.std() != 0 else 0

    return {
        "total_trades": total_trades,
        "total_profit": total_profit,
        "total_loss": total_loss,
        "win_rate": win_rate,
        "max_loss": max_loss,
        "max_drawdown": max_drawdown,
        "max_drawdown_pct": max_drawdown_pct,
        "trades": trades,
        "equity_series": equity_series,
        "initial_capital": initial_capital,
        "final_capital": equity_series.iloc[-1],
        "profit_loss_ratio": profit_loss_ratio,
        "sharpe_ratio": sharpe_ratio
    }

if __name__ == "__main__":
    import yfinance as yf
    df = yf.download("NQ=F", period="30d", interval="5m", auto_adjust=True)
    df = df[['Open','High','Low','Close','Volume']]
    result = backtest_strategy(df)
    print("測試回測結果:", result)
