"""
檔名：b2_sequence_test.py
說明：
1. 檢查單個序列是否為 B2 序列（任意兩個元素的和都不重複）。
2. 多次隨機測試，統計 B2 序列出現的次數與比例。
"""

import random

def is_b2_sequence(seq):
    """檢查序列是否為 B2 序列"""
    seen_sum = set()
    n = len(seq)

    for i in range(n):
        for j in range(i, n):
            s = seq[i] + seq[j]
            if s in seen_sum:
                return False
            seen_sum.add(s)
    return True

def test_b2_sequences(trials=1000, seq_len=5, max_num=100):
    """隨機測試多次 B2 序列"""
    success = 0
    for _ in range(trials):
        nums = list(range(1, max_num))
        random.shuffle(nums)
        test_seq = nums[:seq_len]
        if is_b2_sequence(test_seq):
            success += 1
    print(f"測試 {trials} 次，序列長度 {seq_len}：")
    print(f"B2 序列數量 = {success}")
    print(f"比例 = {success / trials:.2%}")

if __name__ == "__main__":
    # 單次測試
    nums = list(range(1, 100))
    random.shuffle(nums)
    test_seq = nums[:5]
    print("測試序列:", test_seq)
    print("是否為 B2 序列:", is_b2_sequence(test_seq))

    print("\n--- 多次隨機測試 ---")
    test_b2_sequences(trials=1000, seq_len=5, max_num=100)


"""

測試序列: [25, 19, 7, 69, 20]
是否為 B2 序列: True

--- 多次隨機測試 ---
測試 1000 次，序列長度 5：
B2 序列數量 = 757
比例 = 75.70%
"""
