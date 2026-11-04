"""Задание C: проверка своих функций против эталона"""

import random
from src.lab07.search import linear_search, binary_search, two_sum_brute, two_sum_fast
from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort

def check_sorting(fn, trials: int = 100) -> int:
    """Проверяет функцию сортировки на случайных данных против эталонного sorted().
    Принимает конкретную функцию для проверки и кол-во испытаний(по умолчанию 100).
    Возвращает кол-во успешно пройденных тестов
    """
    for _ in range(trials):
        n = random.randint(0,50)
        nums = [random.randint(-100, 100) for _ in range(n)]
        original = list(nums)
        result = fn(nums)
        assert result == sorted(nums), f"{fn.__name__} ошиблась на {nums}: получено {result}, ожидалось {sorted(nums)}"
        assert nums == original, f"{fn.__name__} изменила исходный список"
    return trials

def check_search(trials: int = 100) -> int:
    """Проверяет функции linear_search и binary_search на случайных данных.
    Возвращает количество успешно пройденных испытаний.
    """
    for _ in range(trials):
        n = random.randint(0,50)
        nums = [random.randint(-50,50) for _ in range(n)]
        x = random.randint(-60,60)

        # Линейный поиск против list.index
        try:
            expected_lin = nums.index(x)
        except ValueError:
            expected_lin = -1 #если числа нет, то правильный ответ(эталон) =-1
        actual_lin = linear_search(nums, x)
        assert actual_lin == expected_lin, f"linear_search щшиблась для поиска {x} в {nums}: получено {actual_lin}, ожидалось {expected_lin}"

        # Бинарный поиск
        sorted_nums = sorted(nums)
        try:
            expected_bin = sorted_nums.index(x)
        except ValueError:
            expected_bin = -1
        actual_bin = binary_search(sorted_nums, x)
        if expected_bin == -1:
            assert actual_bin == -1, f"binary_search не нашла элемент, которого нет: {x} в {sorted_nums}"
        else:
            assert actual_bin != -1 and sorted_nums[actual_bin] == x, f"binary_search вернула некорректный индекс {actual_bin} для {x} в {sorted_nums}"

    # редкие случаи
    assert binary_search([], 5) == -1
    assert binary_search([5], 5) == 0
    assert binary_search([5], 7) == -1
    assert binary_search([1, 3], 3) == 1

    return trials


    