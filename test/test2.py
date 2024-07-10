nums = [1,9,5,6]

copy_nums = nums[:]

for num in copy_nums:
    nums.remove(num)
    nums.append(num)
    print(nums)