import pandas as pd

def backtest_strategy(df, ma_short=60, ma_long=120, stop_loss_usd=350,
                      initial_capital=50000, max_lots=3, risk_per_trade=2000,
                      point_value=20):
    df = df.copy()
    # 計算均線
    df['MA_short'] = df['Close'].rolling(window=ma_short).mean()
    df['MA_long']  = df['Close'].rolling(window=ma_long).mean()

    # 計算 MACD
    short_ema = df['Close'].ewm(span=12, adjust=False).mean()
    long_ema  = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = short_ema - long_ema
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # 交易邏輯略 (保留你原本程式碼)
    ...
    return {
        'total_trades': total_trades,
        'total_profit': total_profit,
        'total_loss': total_loss,
        'win_rate': win_rate,
        'max_loss': max_loss,
        'max_drawdown': max_drawdown,
        'max_drawdown_pct': max_drawdown_pct,
        'trades': trades,
        'equity_series': equity_series,
        'initial_capital': initial_capital,
        'final_capital': final_capital,
        'profit_loss_ratio': profit_loss_ratio,
        'sharpe_ratio': sharpe_ratio
    }
