"""
檔名：combination_example.py
說明：生成一個數列中長度為 k 的所有組合，並先打亂原始數列。
適合用來練習遞迴與組合生成。
"""
import random

nums = list(range(1,6))
k = 2
result = []

random.shuffle(nums)  #使用random亂數打亂

def gen(index, path):  #遞迴生成組合
    if len(path) == k:
        result.append(path[:])
        return
    for i in range(index, len(nums)):
        gen(i + 1, path + [nums[i]])

gen(0, [])  ## 呼叫遞迴函式

print("打亂後 nums:", nums)
print("所有組合:", result)




"""
打亂後 nums: [5, 1, 4, 2, 3]
所有組合: [[5, 1], [5, 4], [5, 2], [5, 3], [1, 4], [1, 2], [1, 3], [4, 2], [4, 3], [2, 3]]
"""
