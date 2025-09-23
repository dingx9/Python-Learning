def get_nonnegative_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("輸入錯誤：數字不能小於 0，請再試一次。")
                continue
            return value
        except ValueError:
            print("輸入錯誤：請輸入正整數。")
