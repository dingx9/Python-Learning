#. 用 np.random.choice 抽樣 n次，然後用布林篩選抽到 'A' 的所有結果，布林索引用法。




import numpy as np

#  模擬抽樣
arr = np.array(['A', 'B', 'C'])
p = [0.7, 0.2, 0.1]

# 抽樣 n 次
n = int(input("請輸入抽樣次數: "))
result = np.random.choice(arr, size=n, p=p)
print("抽樣結果前 20 個：", result[:20])

#  建立布林條件：只留下 'A'
mask = result == 'A'
print("布林陣列前 20 個：", mask[:20])

#  使用布林陣列篩選
filtered = result[mask]
has_other_than_A = np.any(filtered != 'A')
print("除了 'A' 還有其他元素嗎？", has_other_than_A)
print("總共有多少個 'A'：", len(filtered))
