import yfinance as yf
import matplotlib.pyplot as plt
from backtest import backtest_strategy
from optimize import run_optimization

# 下載資料
ticker = "NQ=F"
df = yf.download(ticker, period="30d", interval="5m", auto_adjust=True)
df.index = df.index.tz_localize(None)
df = df[['Open','High','Low','Close','Volume']]

# 優化參數
best_params = run_optimization(df, n_trials=50)
print("最佳參數:", best_params)

# 回測
result = backtest_strategy(df, **best_params)

# 列印績效
print(f"總交易次數: {result['total_trades']}")
print(f"最後資金總額: {result['final_capital']:.2f} 美金")
# 交易明細略...

# 繪圖
plt.figure(figsize=(12,6))
plt.plot(result['equity_series'], label='累積資金 (USD)')
plt.fill_between(result['equity_series'].index,
                 result['equity_series'],
                 result['equity_series'].cummax(),
                 color='red', alpha=0.3, label='回撤')
plt.legend()
plt.show()
