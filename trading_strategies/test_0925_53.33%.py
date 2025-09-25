import pandas as pd
import plotly.graph_objects as go

# 假設 df 已經有資料，且包含 ['Open','High','Low','Close']
# 並且時間索引已經設置好

# ----------------------------
# 計算技術指標
# ----------------------------
df['MA60'] = df['Close'].rolling(window=60).mean()
df['MA120'] = df['Close'].rolling(window=120).mean()

short_ema = df['Close'].ewm(span=12, adjust=False).mean()
long_ema = df['Close'].ewm(span=26, adjust=False).mean()
df['MACD'] = short_ema - long_ema
df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

# ----------------------------
# 記錄每筆交易的詳細資料
# ----------------------------
trades = []
position = None
entry_price = 0
entry_time = None

for i in range(120, len(df)):  
    price = df['Close'].iloc[i]


    # ------------------ 買入條件 ------------------
   

    # ------------------ 賣出條件 ------------------
    

# ----------------------------
# 計算績效
# ----------------------------
total_trades = len(trades)
total_profit = sum(t['profit'] for t in trades if t['profit'] > 0)
total_loss   = sum(t['profit'] for t in trades if t['profit'] < 0)
win_trades   = sum(1 for t in trades if t['profit'] > 0)
win_rate     = win_trades / total_trades * 100 if total_trades>0 else 0
max_loss     = min((t['profit'] for t in trades), default=0)

print(f"總交易次數: {total_trades}")
print(f"總盈利: {total_profit:.2f}")
print(f"總虧損: {total_loss:.2f}")
print(f"勝率: {win_rate:.2f}%")
print(f"最大單筆虧損: {max_loss:.2f}")

# ----------------------------
# 列出每筆交易明細
# ----------------------------
for t in trades:
    holding_time = t['exit_time'] - t['entry_time']
    pct_change = (t['profit'] / t['entry_price']) * 100
    print(f"{t['entry_time']} 買 @ {t['entry_price']:.2f} | "
          f"{t['exit_time']} 賣 @ {t['exit_price']:.2f} | "
          f"盈虧: {t['profit']:.2f} ({pct_change:.2f}%) | 持倉時間: {holding_time}")

# ----------------------------
# 畫圖 (K 線 + MA + 買賣點)
# ----------------------------
fig = go.Figure()

# K線
fig.add_trace(go.Candlestick(
    x=df.index,
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close'],
    name="K線"
))

# MA60 / MA120
fig.add_trace(go.Scatter(x=df.index, y=df['MA60'], line=dict(color='blue', width=1), name="MA60"))
fig.add_trace(go.Scatter(x=df.index, y=df['MA120'], line=dict(color='orange', width=1), name="MA120"))

# 買賣點
for trade in trades:
    fig.add_trace(go.Scatter(
        x=[trade['entry_time']], y=[trade['entry_price']],
        mode='markers+text',
        marker=dict(symbol='triangle-up', color='green', size=12),
        text=[f"Buy<br>{trade['entry_price']:.2f}"],
        textposition="bottom center",
        name="Buy"
    ))
    fig.add_trace(go.Scatter(
        x=[trade['exit_time']], y=[trade['exit_price']],
        mode='markers+text',
        marker=dict(symbol='triangle-down', color='red', size=12),
        text=[f"Sell<br>{trade['exit_price']:.2f}"],
        textposition="top center",
        name="Sell"
    ))

fig.update_layout(title="MA+MACD 策略回測", xaxis_rangeslider_visible=False)
fig.show()






# 總交易次數: 15
# 總盈利: 754.75
# 總虧損: -230.25
# 勝率: 53.33%
# 最大單筆虧損: -100.25
# 2025-09-08 17:15:00+00:00 買 @ 23802.00 | 2025-09-08 20:40:00+00:00 賣 @ 23794.25 | 盈虧: -7.75 (-0.03%) | 持倉時間: 0 days 03:25:00
# 2025-09-09 01:05:00+00:00 買 @ 23809.50 | 2025-09-09 13:20:00+00:00 賣 @ 23818.25 | 盈虧: 8.75 (0.04%) | 持倉時間: 0 days 12:15:00
# 2025-09-09 13:30:00+00:00 買 @ 23842.75 | 2025-09-10 12:15:00+00:00 賣 @ 23949.50 | 盈虧: 106.75 (0.45%) | 持倉時間: 0 days 22:45:00
# 2025-09-10 14:00:00+00:00 買 @ 23963.00 | 2025-09-10 18:20:00+00:00 賣 @ 23862.75 | 盈虧: -100.25 (-0.42%) | 持倉時間: 0 days 04:20:00
# 2025-09-11 05:20:00+00:00 買 @ 23888.25 | 2025-09-12 01:00:00+00:00 賣 @ 24011.00 | 盈虧: 122.75 (0.51%) | 持倉時間: 0 days 19:40:00
# 2025-09-12 06:50:00+00:00 買 @ 24018.00 | 2025-09-12 10:50:00+00:00 賣 @ 24017.75 | 盈虧: -0.25 (-0.00%) | 持倉時間: 0 days 04:00:00
# 2025-09-12 20:10:00+00:00 買 @ 24111.50 | 2025-09-15 02:40:00+00:00 賣 @ 24118.00 | 盈虧: 6.50 (0.03%) | 持倉時間: 2 days 06:30:00
# 2025-09-15 10:25:00+00:00 買 @ 24122.75 | 2025-09-15 10:40:00+00:00 賣 @ 24118.75 | 盈虧: -4.00 (-0.02%) | 持倉時間: 0 days 00:15:00
# 2025-09-15 18:50:00+00:00 買 @ 24266.50 | 2025-09-16 14:30:00+00:00 賣 @ 24302.00 | 盈虧: 35.50 (0.15%) | 持倉時間: 0 days 19:40:00
# 2025-09-16 22:55:00+00:00 買 @ 24546.00 | 2025-09-17 08:45:00+00:00 賣 @ 24499.75 | 盈虧: -46.25 (-0.19%) | 持倉時間: 0 days 09:50:00
# 2025-09-17 09:30:00+00:00 買 @ 24525.75 | 2025-09-18 22:40:00+00:00 賣 @ 24716.00 | 盈虧: 190.25 (0.78%) | 持倉時間: 1 days 13:10:00
# 2025-09-19 04:45:00+00:00 買 @ 24715.00 | 2025-09-22 05:30:00+00:00 賣 @ 24849.75 | 盈虧: 134.75 (0.55%) | 持倉時間: 3 days 00:45:00
# 2025-09-22 05:35:00+00:00 買 @ 24850.00 | 2025-09-23 03:05:00+00:00 賣 @ 24999.50 | 盈虧: 149.50 (0.60%) | 持倉時間: 0 days 21:30:00
# 2025-09-23 05:20:00+00:00 買 @ 25000.50 | 2025-09-23 13:40:00+00:00 賣 @ 24954.50 | 盈虧: -46.00 (-0.18%) | 持倉時間: 0 days 08:20:00
# 2025-09-24 00:20:00+00:00 買 @ 24838.50 | 2025-09-24 14:40:00+00:00 賣 @ 24812.75 | 盈虧: -25.75 (-0.10%) | 持倉時間: 0 days 14:20:00
