# python_labs

# Лабораторная работа 4 - Файлы: TXT/CSV и отчеты по текстовой статистике

## Задание A — модуль ввода/вывода `src/lab04/io_txt_csv.py`

### 1.Функция `read_text`

```python
import csv
from pathlib import Path

def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    p = Path(path)

    '''Читает файл и возвращает его содержимое одной строкой.

    Args: 
        path: путь к файлу
        encoding: кодировка файла(пример: encoding="cp1251"), по умолчанию UTF-8
    Returns:
        Прочитанный файл в виде строки
    '''

    return p.read_text(encoding=encoding)
```
Функция читает файл целиком и возвращает содержимое в виде одной строки. По умолчанию используется кодировка UTF-8. Внутри функции создается объект Path  из переданного пути. Если файл не найден, возникает `FileNotFoundError`. При несовпадении кодировки возникает `UnicodeDecodeError`.

### 2.Функция `ensure_parent_dir`

```python
def ensure_parent_dir(path: str | Path) -> None:
    '''Создаем родительские папки, если их еще нет.
    Args: 
        path: путь к файлу
    Returns:
        None
    '''
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
```
Данная функция должна гарантировать, что папка, в которой будет лежать файл, существует. Принимает на вход либо строку, либо объект(Path). Ничего не возвращает, просто выполняет действие(создает папки).

### 3. Функция `write_csv`

```python
def write_csv(rows: list[tuple | list], path: str | Path, header: tuple[str, ...] | None=None) -> None:
    '''Записывает список строк, кортежей или списков в csv-файл с разделителем-запятой.
    Args:
        rows: строки таблицы; все должны быть одной длины
        path: путь к файлу 
        header: заголовок таблицы. если передан, пишется первой строкой.

    Returns:
        None
    
    Raises:
        ValueError: Строки разной длины
    '''
    rows = list(rows)
    if not rows:
        standart = len(header) if header is not None else 0
    else:
        standart = len(rows[0]) if header is None else len(header)

    for r in rows:
        if len(r) != standart:
            raise ValueError('Все строки доожны быть одинаковой длины')
        
    ensure_parent_dir(path=path)
    p = Path(path)

    with p.open("w", newline="", encoding="utf-8") as file:
        w = csv.writer(file)
        if header:
            w.writerow(header)
        for r in rows:
            w.writerow(r)
```
Функция записывает строки в CSV-файл. Перед записью проверяется, что: если нет строк, то за эталонную длину берем заголовок, если он есть(если его нет-выводим 0); если строки есть, то за эталонную длину берем длину первой строки, если заголовка нет(если он есть-берем длину заголовка). Если передан параметр `header`, он записывается первой строкой файла.

![Картинка 1](/image/lab04/testkeys1_lab04.png)
*Рис.1 Проверка тест-кейсов

![Картинка 2](/image/lab04/primer1_lab04.png)

![Картинка 3](/image/lab04/primer2_lab04.png)

*Рис.2 Результат записи 


## Задание B - скрипт статистики `src/lab04/text_report.py`

### Исходный код
```python
from src.lab04.io_txt_csv import read_text, write_csv, ensure_parent_dir
from lib.text import normalize, tokenize, top_n, count_freq
import argparse
from pathlib import Path

def generate_report(input_path, output_path):
    text = read_text(input_path)   #читаем текст
    normal_text = normalize(text)  #нормализуем 
    tokens = tokenize(normal_text) #разбиваем на слова(токены)
    freq = count_freq(tokens)      #считаем частоту слов
    top_words = top_n(freq, 5)     #берем топ-5 слов

    write_csv(top_words, output_path, header=("word", "count"))

    total_words = len(tokens) #общее кол-во слов
    unique_words = len(freq)  #кол-во уникальных слов

    print(f"Всего слов: {total_words}")
    print(f"Уникальных слов: {unique_words}")
    print("Топ-5:")
    for word, count in top_words:
        print(f"{word}:{count}")
```
Объявляем функцию: указываем путь к входному файлу и путь, куда сохранить CSV. Записываем CSV с помощью функции. Берем все слова с частотами, путь и заголовок.

### Проверка тест-кейсов
#### Тест A
```python
def run_test_a():
    '''Тест А: обычный файл с текстом'''
    print("\n" + "="*40)
    print("ТЕСТ А: Один файл")
    print("="*40)

    input_file = "data/lab04/input.txt"
    output_file = "data/lab04/report.csv"

    ensure_parent_dir(input_file)
    Path(input_file).write_text("Привет, мир, привет!!!", encoding = "utf-8")

    #Запускаем генерацию
    generate_report(input_file, output_file)

    #Проверяем CSV
    print("\n---Проверка report.csv---")
    actual_csv = read_text(output_file)
    expected_csv = "word,count\nпривет,2\nмир,1\n"
    if actual_csv==expected_csv:
        print("CSV совпадает с ожидаемым!")
    else:
        print("Ошибка! CSV не совпадает с ожидаемым")
```
В переменные записываем пути откуда читать текст и куда сохранить CSV. Создаем текстовый файл с помощью функции, которая создает родительские папки, если их нет. `Path(input_file).write_text` создает файл `input.txt` и записыват в него текст. Проверка: читаем содержимое созданного файла; задаем эталонную строку; сравниваем реальный результат с эталоном.

![](/image/lab04/testA_lab04.png)

#### Тест B
```python
def run_test_b_empty():
    '''Тест B: пустой файл'''
    print("\n" + "="*40)
    print("ТЕСТ B: Пустой файл")
    print("="*40)

    input_file = "data/lab04/empty.txt"
    output_file = "data/lab04/report_empty.csv"

    #Создаем пустой входной файл
    write_csv([],input_file)
    #Запускаем генерацию
    generate_report(input_file,output_file)

    #Проверяем CSV
    print("\n---Проверка report_empty.csv---")
    actual_csv = read_text(output_file)
    expected_csv = "word,count\n"
    if actual_csv==expected_csv:
        print("CSV корректен")
    else:
        print("CSV не совпадает")

if __name__ == "__main__":
    run_test_a()
    run_test_b_empty()
```
Создаем пустой файл с помощью функции `write_csv`(передаем пустой список и путь). Аналогично тесту А проверяем корректность CSV.

![](/image/lab04/testB_lab04.png)

