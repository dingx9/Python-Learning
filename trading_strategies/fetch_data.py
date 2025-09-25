
#################   ＮＱ 歷史資料下載  

# 安裝 yfinance
!pip install yfinance --quiet

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from google.colab import files

# ----------------------------
# 參數設定
# ----------------------------
ticker = "NQ=F"  # 那斯達克期貨
interval = "5m"  # 5 分鐘 K 線
days = 15        # 抓最近 15 天
end_date = datetime.utcnow()  # 以今天為結束
start_date = end_date - timedelta(days=days)

# ----------------------------
# 下載資料
# ----------------------------
print("開始抓取資料...")
df = yf.download(
    tickers=ticker,
    start=start_date.strftime("%Y-%m-%d"),
    end=end_date.strftime("%Y-%m-%d"),
    interval=interval,
    auto_adjust=True
)

if df.empty:
    print("沒有抓到資料，請確認時間或市場是否開盤")
else:
    print("抓取完成，資料前 5 筆：")
    print(df.head())

    # ----------------------------
    # 存 CSV
    # ----------------------------
    csv_filename = f"{ticker}_last_{days}days_{interval}.csv"
    df.to_csv(csv_filename)
    print(f"已存成 CSV 檔案: {csv_filename}")

    # ----------------------------
    # Colab 下載
    # ----------------------------
    # files.download(csv_filename)
