def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    if not nums:
        raise ValueError
    nums.sort()
    return nums[0],nums[-1]


def unique_sorted(nums: list[float | int]) -> list[float | int]:

    uni_nums = []
    for num in nums:
        if num not in uni_nums:
            uni_nums.append(num)
    n = len(uni_nums)
    for i in range(n):
        for j in range(n-i-1):
            if uni_nums[j]>uni_nums[j+1]:
                uni_nums[j],uni_nums[j+1]=uni_nums[j+1],uni_nums[j]
    return uni_nums
    


def flatten(mat: list[list | tuple])-> list:
    fl = []
    for i in mat:
        if type(i) == list or type(i) == tuple:
            fl.extend(i)
        else:
            raise TypeError
    return fl
'''
print(min_max([3,-1,5,5,0]))
print(min_max([42]))
print(min_max([-5,-2,-9]))
print(min_max([1.5,2,2.0,-3.1]))
try:
    print(min_max([]))
except ValueError:
    print("ValueError")
'''

print(unique_sorted([3,1,2,1,3]))
print(unique_sorted([]))
print(unique_sorted([-1,-1,0,2,2]))
print(unique_sorted([1.0,1,2.5,2.5,0]))

'''
print(flatten([[1,2],[3,4]]))
print(flatten([[1,2],(3,4,5)]))
print(flatten([[1],[],[2,3]]))
print(flatten([[1,2],"ab"]))
'''