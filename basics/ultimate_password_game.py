# 檔名：ultimate_password_game.py
# 說明：終極密碼猜數字遊戲，提示範圍隨猜測自動縮小，並判斷奇偶數



import random

def ultimate_password_game(min_num=1, max_num=100):
    """終極密碼遊戲"""
    secret = random.randint(min_num, max_num)
    guess = None
    tries = 0

    current_min = min_num
    current_max = max_num

    print(f"=== 終極密碼 ===")
    print(f"提示：數字在 {min_num} 到 {max_num} 之間")

    while guess != secret:
        try:
            guess = int(input(f"請輸入你的猜測 ({current_min}~{current_max}): "))
        except ValueError:
            print("輸入錯誤，請輸入整數！")
            continue

        # 判斷是否在指定範圍
        if guess < current_min or guess > current_max:
            print(f"請輸入 {current_min} 到 {current_max} 之間的數字！")
            continue

        tries += 1

        # 判斷大小
        if guess < secret:
            print("太小了！")
            current_min = guess  # 更新最小範圍
        elif guess > secret:
            print("太大了！")
            current_max = guess  # 更新最大範圍
        else:
            print(f"哈哈哈你爆掉了！數字就是 {secret}")
            print(f"你總共猜了 {tries} 次")
            # 奇偶檢查
            print("答案是偶數 " if secret % 2 == 0 else "答案是奇數 ")

if __name__ == "__main__":
    ultimate_password_game(1,50)
