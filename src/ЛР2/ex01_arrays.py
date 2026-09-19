def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    if not nums:
        raise ValueError
    return min(nums), max(nums)


def unique_sorted(nums: list[float | int]) -> list[float | int]:
    return sorted(set(nums))


def flatten(mat: list[list | tuple])-> list:
    fl = []
    for i in mat:
        if type(i) == list or type(i) == tuple:
            fl.extend(i)
        else:
            raise TypeError
        return fl


print(min_max([3,-1,5,5,0]))
print(min_max([42]))
print(min_max([-5,-2,-9]))
print(min_max([1.5,2,2.0,-3.1]))
try:
    print(min_max([]))
except ValueError:
    print("ValueError")