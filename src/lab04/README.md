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
