import random

nums = list(range(1,5))
k = 2
result = []

random.shuffle(nums)

def gen(index, path):
    if len(path) == k:
        result.append(path[:])
        return
    for i in range(index, len(nums)):
        gen(i + 1, path + [nums[i]])

gen(0, [])

print("打亂後 nums:", nums)
print("所有組合:", result)
