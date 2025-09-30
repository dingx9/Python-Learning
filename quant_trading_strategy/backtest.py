import pandas as pd
import yfinance as yf
from utils import calculate_sharpe, calculate_drawdown, calculate_profit_loss_ratio

POINT_VALUE = 20  # 每口每點價值美元

def backtest_strategy(df, ma_short=60, ma_long=120, stop_loss_usd=350,
                      initial_capital=50000, max_lots=3, risk_per_trade=2000):
    df = df.copy()
    df['MA_short'] = df['Close'].rolling(ma_short).mean()
    df['MA_long']  = df['Close'].rolling(ma_long).mean()

    short_ema = df['Close'].ewm(span=12, adjust=False).mean()
    long_ema  = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = short_ema - long_ema
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    trades = []
    position = None
    entry_price = 0
    entry_time = None
    entry_lots = 0
    capital = 0
    equity_curve = []

    for i in range(ma_long, len(df)):
        price = df['Close'].iloc[i]

        is_bull = (df['Close'].iloc[i-30:i] > df['MA_long'].iloc[i-30:i]).all()
        rising3 = df['Close'].iloc[i-3] < df['Close'].iloc[i-2] < df['Close'].iloc[i-1]
        macd_neg = df['MACD'].iloc[i] < 0
        cross_short = df['Close'].iloc[i] > df['MA_short'].iloc[i] and df['Close'].iloc[i-1] <= df['MA_short'].iloc[i-1]
        cross_long  = df['Close'].iloc[i] > df['MA_long'].iloc[i]  and df['Close'].iloc[i-1] <= df['MA_long'].iloc[i-1]

        # 買入條件
        if position is None and macd_neg and (cross_short or cross_long) and is_bull and rising3:
            allowed_lots = risk_per_trade / stop_loss_usd
            entry_lots = max(1, min(max_lots, int(allowed_lots)))
            position = 1
            entry_price = price
            entry_time = df.index[i]

        # 賣出條件
        if position is not None:
            sell = False
            if price <= entry_price - stop_loss_usd / POINT_VALUE:
                sell = True
            elif df['MA_short'].iloc[i] < df['MA_long'].iloc[i] and df['MA_short'].iloc[i-1] >= df['MA_long'].iloc[i-1]:
                sell = True

            if sell:
                profit_points = price - entry_price
                profit_usd = profit_points * POINT_VALUE * entry_lots
                trades.append({
                    'entry_time': entry_time,
                    'entry_price': entry_price,
                    'exit_time': df.index[i],
                    'exit_price': price,
                    'profit': profit_usd,
                    'holding_time': df.index[i] - entry_time,
                    'lots': entry_lots
                })
                capital += profit_usd
                position = None

        current_equity = initial_capital + capital + ((price - entry_price) * POINT_VALUE * entry_lots if position else 0)
        equity_curve.append(current_equity)

    equity_series = pd.Series(equity_curve)
    total_trades = len(trades)
    win_trades = sum(1 for t in trades if t['profit'] > 0)
    win_rate = win_trades / total_trades * 100 if total_trades > 0 else 0
    max_loss = min((t['profit'] for t in trades), default=0)
    max_dd, max_dd_pct = calculate_drawdown(equity_series)
    profit_loss_ratio = calculate_profit_loss_ratio(trades)
    sharpe_ratio = calculate_sharpe(equity_series)

    return {
        'total_trades': total_trades,
        'win_rate': win_rate,
        'max_loss': max_loss,
        'max_drawdown': max_dd,
        'max_drawdown_pct': max_dd_pct,
        'trades': trades,
        'equity_series': equity_series,
        'initial_capital': initial_capital,
        'final_capital': equity_series.iloc[-1],
        'profit_loss_ratio': profit_loss_ratio,
        'sharpe_ratio': sharpe_ratio
    }
