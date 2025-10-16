import numpy as np
from collections import Counter

arr = ['A', 'B', 'C']
p = [0.7, 0.2, 0.1]     #裡面的數加起來要＝1


result = np.random.choice(arr, size=100000, p=p)

# 統計每個元素出現次數
count = Counter(result)


# 計算實際機率並四捨五入到小數第二位
probabilities_rounded = {k: round(v / len(result), 2) for k, v in count.items()}


print("出現次數：", count)
print("實際機率：", probabilities)
