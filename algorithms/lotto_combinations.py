"""
檔名：lotto_combinations.py
說明：
1. 生成隨機 6 個樂透號碼（從 1~49 隨機挑選，不重複）。
2. 從中找出所有 3 個號碼組合。
3. 篩選條件：組合總和 < 50 且所有號碼為偶數。
"""

import random
import time

# ---- 計時開始 ----
start = time.time()

# 1. 生成 1~49 的數字，並隨機打亂
nums = list(range(1, 50))
random.shuffle(nums)

# 2. 取前 6 個號碼作為樂透號碼
lotto = nums[:6]
print("隨機選號:", lotto)

# 3. 遞迴產生組合
k = 3
result = []

def gen(index, path):
    """遞迴生成組合，並套用篩選條件"""
    if len(path) == k:
        # 先檢查是否全為偶數，再檢查總和
        if all(x % 2 == 0 for x in path) and sum(path) < 50:
            result.append(path[:])
        return

    for i in range(index, len(lotto)):
        gen(i + 1, path + [lotto[i]])

# 呼叫遞迴函式
gen(0, [])

# 4. 輸出結果
print("符合條件的 3 個號碼組合:", result)

# ---- 計時結束 ----
end = time.time()
print(f"程式執行時間: {end - start:.6f} 秒")

