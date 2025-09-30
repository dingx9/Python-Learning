import pandas as pd

def backtest_strategy(df, ma_short=60, ma_long=120, stop_loss_usd=350,
                      initial_capital=50000, max_lots=3, risk_per_trade=2000,
                      point_value=20):
    # ... 你的回測策略邏輯（完整保留）
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
        "final_capital": final_capital,
        "profit_loss_ratio": profit_loss_ratio,
        "sharpe_ratio": sharpe_ratio
    }

if __name__ == "__main__":
    import yfinance as yf

    df = yf.download("NQ=F", period="30d", interval="5m", auto_adjust=True)
    df = df[['Open','High','Low','Close','Volume']]

    result = backtest_strategy(df)
    print("測試回測結果:", result)
