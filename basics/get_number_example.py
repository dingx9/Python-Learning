 # basics/get_number.py


def get_number(prompt):
    """
    要求使用者輸入 1~50 之間的整數，最多嘗試 3 次。
    超過 3 次錯誤或輸入不合法則返回 None。
    """

    attempts = 0
    while True:
        if attempts >= 3:
            print("錯誤次數過多，程式結束")
            return None
        try:
            value = int(input(prompt))
            if value > 50 or value < 1:
                print("請輸數1-50之間的數")
                attempts += 1
                continue
            return value
        except ValueError:
            print("數入錯誤")
            attempts += 1

x = get_number("請輸數1-50之間的數: ")
print("你輸入的數為:", x)
