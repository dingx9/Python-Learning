import numpy as np
from collections import Counter



# ------------------------------
# 1.抽樣
# 用 np.random.choice 從 ['A','B','C'] 抽 n 次
# 結果存到 result 陣列
# ------------------------------

# ------------------------------
# 2.建立布林條件
# 用 result == 'A' 產生布林陣列 mask
# True 表示該位置是 'A'，False 表示不是
# ------------------------------

# ------------------------------
# 3.篩選陣列
# 用 filtered = result[mask] 只留下 True 對應的元素
# 這就是只保留 'A' 的結果
# ------------------------------

# ------------------------------
# 4.檢查其他元素
# 用 np.any(filtered != 'A')
# 如果 True → 表示篩選後還有其他元素（理論上不會）
# 如果 False → 只剩 'A'
# ------------------------------

# ------------------------------
# 5.用 Counter(result) 計算每個元素出現次數
# ------------------------------

# ------------------------------
# 6.計算機率
# 用字典推導式 v / len(result)
# 再用 round(..., 2) 四捨五入到小數第二位
# ------------------------------


# 模擬抽樣
arr = np.array(['A', 'B', 'C'])
p = [0.7, 0.2, 0.1]

# 抽樣 n 次
n = int(input("請輸入抽樣次數: "))
result = np.random.choice(arr, size=n, p=p)
#print("抽樣結果前 20 個：", result[:20])

# 建立布林條件：只留下 'A'
mask = result == 'A'
#print("布林陣列前 20 個：", mask[:20])

# 使用布林陣列篩選
filtered = result[mask]

#print("a",filtered[:20])
# 檢查篩選後的結果裡是否有其他元素（這裡應該都是 'A'）
has_other_than_A = np.any(filtered != 'A')
print("除了 'A' 還有其他元素嗎？", has_other_than_A)
print("總共有多少個 'A'：", len(filtered))

# 計算每個元素出現次數
count = Counter(result)

# 計算實際機率並四捨五入到小數第二位
probabilities = {k: round(v / len(result), 2) for k, v in count.items()}

print("出現次數：", count)
print("實際機率（四捨五入到小數第二位）：", probabilities)
