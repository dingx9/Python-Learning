import pandas as pd
import numpy as np
from utils import calculate_metrics

def backtest_strategy(df, ma_short=60, ma_long=120, stop_loss_usd=350,
                      initial_capital=50000, max_lots=3, risk_per_trade=2000,
                      point_value=20):
    df = df.copy()

    # 均線
    df['MA_short'] = df['Close'].rolling(window=ma_short).mean()
    df['MA_long']  = df['Close'].rolling(window=ma_long).mean()

    trades = []
    equity = [initial_capital]
    position = 0
    entry_price = 0
    lots = 0

    for i in range(len(df)):
        if pd.isna(df['MA_short'].iloc[i]) or pd.isna(df['MA_long'].iloc[i]):
            equity.append(equity[-1])
            continue

        price = df['Close'].iloc[i]
        current_capital = equity[-1]

        # 開倉條件
        if position == 0:
            if df['MA_short'].iloc[i] > df['MA_long'].iloc[i]:
                lots = min(max_lots, int(current_capital / risk_per_trade))
                position = 1
                entry_price = price
            elif df['MA_short'].iloc[i] < df['MA_long'].iloc[i]:
                lots = min(max_lots, int(current_capital / risk_per_trade))
                position = -1
                entry_price = price

        # 平倉條件
        else:
            pnl = (price - entry_price) * point_value * lots * position
            if pnl <= -stop_loss_usd:
                current_capital += pnl
                trades.append({"entry": entry_price, "exit": price, "profit": pnl, "lots": lots})
                position = 0
                lots = 0
            elif (position == 1 and df['MA_short'].iloc[i] < df['MA_long'].iloc[i]) or \
                 (position == -1 and df['MA_short'].iloc[i] > df['MA_long'].iloc[i]):
                current_capital += pnl
                trades.append({"entry": entry_price, "exit": price, "profit": pnl, "lots": lots})
                position = 0
                lots = 0

            equity.append(current_capital)
            continue

        equity.append(current_capital)

    return calculate_metrics(np.array(equity), trades)
