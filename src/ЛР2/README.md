# python_labs
# Лабораторная работа 2
## Задание 1

### Сначала проверяем список на пустоту. Если список пуст, выходит исключение ValueError. В противном случае возвращаются встроенные функции

'''
def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    if not nums:
        raise ValueError
    return min(nums), max(nums)
'''
![Картинка 1](./image/ЛР2/ex01.png)