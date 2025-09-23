"""
加權錯誤率計算器
數學公式: WER = sum(errors[i] * weights[i]) / total_samples
- errors: 各類錯誤數量 e_i
- weights: 對應權重 w_i
- total_samples: 總樣本數 N
"""

def weighted_error_rate(errors, weights, total_samples):
    if len(errors) != len(weights):
        raise ValueError("錯誤數量列表和權重列表長度必須相同")
    if total_samples == 0:
        raise ValueError("總樣本數不能為 0")

    # 計算加權總和
    weighted_sum = sum(e * w for e, w in zip(errors, weights))

    # WER 計算
    wer = weighted_sum / total_samples
    return wer

if __name__ == "__main__":
    errors = [5, 10, 15]      # e_i
    weights = [3, 2, 1]       # w_i
    total_samples = 100       # N

    wer = weighted_error_rate(errors, weights, total_samples)

    print("=== 加權錯誤率計算 ===")
    print(f"錯誤數量: {errors}")
    print(f"權重: {weights}")
    print(f"總樣本數: {total_samples}")
    print(f"WER = sum(errors[i]*weights[i])/N = {wer:.2%}")
