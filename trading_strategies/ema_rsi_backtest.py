import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = {
    "date": pd.date_range(start="2025-01-01", periods=50),
    "close": [100,102,101,105,103,108,110,107,111,115,117,116,118,120,
              119,121,125,123,126,128,130,129,131,133,132,134,136,135,
              137,140,138,141,143,142,144,146,147,145,148,150,152,151,
              153,155,154,156,158,157,159,160]
}
df = pd.DataFrame(data)
df['ema'] = df['close'].ewm(span=10, adjust=False).mean()
delta = df['close'].diff()
gain = np.where(delta>0, delta,0)
loss = np.where(delta<0, -delta,0)
avg_gain = pd.Series(gain).rolling(window=14).mean()
avg_loss = pd.Series(loss).rolling(window=14).mean()
rs = avg_gain/avg_loss
df['rsi'] = 100 - (100/(1+rs))
plt.plot(df['date'], df['close'], label='Close Price')
plt.plot(df['date'], df['ema'], label='EMA')
plt.legend()
plt.show()
