"""Задание D: замеры времени через timeit и таблица результатов"""

import random
import timeit
from src.lab04.io_txt_csv import write_csv
from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort
from src.lab07.search import linear_search, binary_search, two_sum_brute, two_sum_fast

def read_numbers(path):
    with open(path, encoding = "utf-8") as f:
        return [int(row["value"] for row in csv.DictReader(f))]

def format_time(seconds): #красиво форматируем время для таблицы
    return f"{seconds:.4f} с" if seconds < 60 else "> 60 с"

def run_benchmark():
    random.seed(42) 
    csv.results = []

#1. БЕНЧМАРК СОРТИРОВОК
sizes_sort = [1000, 10000, 100000]
print("\n--- Бенчмарк сортировок---")
print(f"{'Алгоритм': <15} | {'n':<7} | {'Время':<10}")
print("-" * 40)

for n in sizes_sort:
    #генерируем одни и те же данные для сортировок
    data = [random.randint(-1000, 1000) for _ in range(n)]

#встроенная сортировка(эталон)
t_sorted = timeit.timeit(lambda: sorted(data), number=1)
print(f"{'sorted':<15} | {n:<7} | {format_time(t_sorted):<10}")
csv_results.append(("sort", n, "sorted", t_sorted))

for fn, name in [(bubble_sort, "bubble"), (insertion_sort, "insertion"), (selection_sort, "selection")]:
    if n>=100000:
        print(f"{name:<15} | {n:<7} | > 60 c (пропущено)")
        csv.results.append(("sort", n, name, ">60"))
        continue
    t = timeit.timeit(lambda: fn(data.copy()), number=1)
    print(f"{name:<15} | {n:<7} | {format_time(t):<10}")
    csv_results.append(("sort", n, name, t))

#2. БЕНЧМАРК ПОИСКА
print("\n---Бенчмарк поиска---")
print(f"{'Алгоритм':<15} | {'Запросы':<10} | {'Время':<10}")
print("-"*40)

#создаем список на 100_000 элементов и сортируем его
search_data = [random.randint(-10000, 10000) for _ in range(100000)]
search_sorted = sorted(search_data)
queries = [random.randint(-10000, 10000) for _ in range(10000)] #случайные числа, которые будем искать в массиве

t_linear = timeit.timeit(lambda: [linear_search(search_data, x) for x in queries], number=1)
print(f"{'linear_search':<15} | 10000 | {format_time(t_linear):<10}")
csv_results.append(("search", 100000, "linear_search", t_linear))


