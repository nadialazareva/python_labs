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
    random.seed(42) #чтобы при кажлом запуске генерировались одни и те же данные
    csv_results = []
    headers = ["task", "n", "impl", "seconds"]
    print("\nРезультаты бенчмарка:")
    print(f"{headers[0]:<10} | {headers[1]:<7} | {headers[2]:<15} | {headers[3]:<10}")
    print("-"*52)

#============================================================================================
#1. БЕНЧМАРК СОРТИРОВОК
#============================================================================================
    sizes_sort = [1000, 10000, 100000]

    for n in sizes_sort:
        #генерируем одни и те же данные для сортировок
        data = [random.randint(-1000, 1000) for _ in range(n)]

        #встроенная сортировка(эталон)
        t_sorted = timeit.timeit(lambda: sorted(data), number=1)
        print(f"{'sorting':<10} | {n:<7} | {'sorted':<15} | {format_time(t_sorted):<10}")
        csv_results.append(("sort", n, "sorted", t_sorted))

        for fn, name in [(bubble_sort, "bubble"), (insertion_sort, "insertion"), (selection_sort, "selection")]:
            if n>=100000:
                print(f"{'sorting':<10} | {n:<7} | {name:<15} | {'>60':<10}")
                csv_results.append(("sorting", n, name, ">60"))
                continue
            t = timeit.timeit(lambda: fn(data.copy()), number=1)
            print(f"{'sorting':<10} | {n:<7} | {name:<15} | {format_time(t):<10}")
            csv_results.append(("sorting", n, name, t))

#==================================================================================================
#2. БЕНЧМАРК ПОИСКА
#==================================================================================================

    #создаем список на 100_000 элементов и сортируем его
    search_data = [random.randint(-10000, 10000) for _ in range(100000)]
    search_sorted = sorted(search_data)
    queries = [random.randint(-10000, 10000) for _ in range(10000)] #случайные числа, которые будем искать в массиве

    #Линейный поиск
    t_linear = timeit.timeit(lambda: [linear_search(search_data, x) for x in queries], number=1)
    print(f"{'search':<10} | {10000:<7} | {'linear_search':<15} | {format_time(t_linear):<10}")
    csv_results.append(("search", 100000, "linear_search", t_linear))

    #Бинарный поиск
    #включаем время сортировки отдельной строкой, чтобы рассчитать реальное время бин.поиска
    def sort_and_search():
        s_data = sorted(search_data)
        for x in queries:
            binary_search(s_data, x)
    t_binary = timeit.timeit(sort_and_search, number=1)
    print(f"{'search':<10} | {100000:<7} | {'binary_search':<15} | {format_time(t_binary):<10} (вкл. сортировку)")
    csv_results.append(("search", 100000, "binary_search", t_binary))

#=====================================================================================================
#3. БЕНЧМАРК TWO SUM
#=====================================================================================================

    for n in [1000, 10000]:
        nums = [random.randint(-50,50) for _ in range(n)]
        i, j = random.sample(range(n), 2)
        target = nums[i] + nums[j]

        #замеряем время для медленного алгоритма
        t_brute = timeit.timeit(lambda: two_sum_brute(nums, target), number=1) 
        print(f"{'two_sum':<10} | {n:<7} | {'two_sum_brute':<15} | {format_time(t_brute):<10}")
        csv_results.append(("two_sum", n, "brute", t_brute))

        #замеряем время для быстрого алгоритма
        t_fast = timeit.timeit(lambda: two_sum_fast(nums, target), number=1)
        print(f"{'two_sum':<10} | {n:<7} | {'two_sum_fast':<15} | {format_time(t_fast):<10}")
        csv_results.append(("two_sum", n, "fast", t_fast))

#сохранение результатов
    print("\n---Сохранение данных---")
    try:
        #safe_results = []
        #for row in csv_results:
            #safe_results.append((str(row[0]), str(row[1]), str(row[2]), str(row[3])))
            
        write_csv(rows = csv_results, path = "data/lab07/bench.csv", header = headers)
        print("Результаты сохранены в data/lab07/bench.csv")
    except Exception as e:
        print(f"Ошибка сохранения CSV: {e}")
        for row in csv_results:
            print(row)

if __name__ == "__main__":
    run_benchmark()

# python -m src.lab07.bench


