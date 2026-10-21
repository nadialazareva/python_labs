# python_labs

# Лабораторная работа 5 - JSON, CSV и XLSX

# Структура лабораторой работы

- `src/lab05/json_csv.py` — преобразование JSON в CSV и CSV в JSON;
- `src/lab05/csv_xlsx.py` — преобразование CSV в XLSX.

## Задание А: JSON <-> CSV

### Функция `json_to_csv`
```python
import json
import csv
from pathlib import Path
import sys

def json_to_csv(json_path: str, csv_path: str) -> None:
    ''' Преобразует JSON со списком словарей в CSV
    Отсутствующие поля заполняются пустой строкой
    
    Raises:
        FileNotFoundError: входного файла нет
        ValueError: не то расширение, пустой файл или не список словарей
    '''
    json_file = Path(json_path)
    if not json_file.is_file():
        raise FileNotFoundError(f"Файл не найден: {json_path}")
    
#Создаем объект Path из строки пути. Проверяем, существует ли файл

    try:
        with open(json_file, 'r', encoding = 'utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        raise ValueError("Неверный формат JSON или файл пуст")
    
    if not isinstance(data,list) or not data:
        raise ValueError('JSON должен содержать непустой список объектов(словарей)')
    if not all(isinstance(item,dict) for item in data):
        raise ValueError('Все элементы списка в JSON должны быть словарями')

#Проверка, что в JSON лежит список и он непустой.Проверка,что каждый элемент явл. словрем

    all_keys = set()
    for item in data:
        all_keys.update(item.keys())
    headers = sorted(list(all_keys))

#Порядок колонок - по алфавиту. Во множество добавляем только новые ключи.
#Превращаем множество в список и сортируем по алфавиту

    if not headers:
        raise ValueError('В JSON отсутствуют данные для создания колонок')
    try:
        with open(csv_path, 'w', encoding = 'utf-8', newline = '') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    except Exception as e:
        raise ValueError(f"Ошибка при записи CSV файла: {e}")


#Открываем файл для записи, передаем его в инструмент writer, чтобы записать строки с названиями колонок.
#Берем каждый словарь и вытаскиваем из него только значения по заданным ключам из спика.
#Если ключа не хватает,ставится пробел по умолчанию
```

Что делает функция:
1. Проверяет существование входного файла
2. Проверяет формат (расширение `.json`)
3. Объект является непустым списком словарей
4. Собирает названия всех ключей в алфавитном порядке
5. Проверяет наличие заголовков для создания колонок
6. Записывает заголовок и строки в CSV в кодировке UTF-8

### Функция `csv_to_json`
```python
def csv_to_json(csv_path: str, json_path: str) -> None:
    '''Преобразовать CSV в JSON со списком словарей
    Первая строка в CSV - заголовок

    Raises:
        FileNotFoundError: входного файла нет
        ValueError: не то расширение, нет заголовка или нет ни одной записи
    '''
    csv_file = Path(csv_path)
    if not csv_file.is_file():
        raise FileNotFoundError(f"Файл не найден: {csv_path}")
#Проверяем существование файла

    try:
        with open(csv_file, 'r', encoding = 'utf-8', newline = '') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                raise ValueError('CSV-файл пуст или нет заголовка')
            data = list(reader)
        if not data:
            raise ValueError('CSV-файл не содержит данных(только заголовок)')
        
    except csv.Error as e:
        raise ValueError(f"Ощибка чтения CSV")
    
    try:
        Path(json_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(json_path, 'w', encoding = 'utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except IOError as e:
        raise ValueError(f"Ошибка записи JSON")
```

Что делает функция:
1. Проверяет существование файла
2. `csv.DictResder(f)` автоматически берет первую строку файла и делает из нее ключи(заголовки), остальные строки превращает в словари
3. Объект является непустым
4. `json.dump` записывает файл в формате JSON, чтобы оставались русские буквы.

## Тесты задания А и проверка на совпадение длины

Файлы([Нажми сюда](../../data/)):

![](/image/lab05/testA_lab05.png)

## Задание В: CSV -> XLSX

### Функция `csv_to_xlsx`
```python
import csv
import openpyxl
from openpyxl import Workbook
from pathlib import Path
from openpyxl.utils import get_column_letter

def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    '''Преобразовать CSV в Excel

    Первая строка CSV становится заголовком таблицы, лист называется Sheet1
    Ширина колонки равна длине самого длинного текста

    Raises:
        FileNotFoundError: входного файла нет.
        ValueError: не то расширение или в CSV нет данных.
    '''

    csv_file = Path(csv_path)
    xlsx_file = Path(xlsx_path)
    if not csv_file.is_file():
        raise FileNotFoundError(f"Файл не найден: {csv_path}")
    if csv_file.suffix.lower() != '.csv': #проверяем расширение файла
        raise ValueError(f"Неверный тип файла. Ожидался: csv, получен: {csv_file.suffix}")

    try:
        with open(csv_file, 'r', encoding = 'utf-8') as f:
            reader = csv.reader(f) #читает построчно и превращает каждую строку в список
            data = list(reader) #сохраняет все строки в виде списка списков
    except Exception as e:
        raise ValueError(f"Ошибка чтения CSV: {e}")

    if not data:
        raise ValueError("в CSV файле нет данных")

    try:
        wb = Workbook() #создает в памяти новую книгу Excel
        ws = wb.active #берет первый и единственный лист в книге
        ws.title = "Sheet1"

        for row in data:
            ws.append(row) #записывает каждую строку в блокнот

        #ищем саммый длинный текст в колонке
        wid = {}
        for row in data:
            for i, value in enumerate(row, start=1):
                wid[i] = max(wid.get(i,0), len(value))

        #у нас должна храниться ширина по букве колонки, а не по номеру
        for i, wid in wid.items():
            ws.column_dimensions[get_column_letter(i)].width = max(wid, 8)
        wb.save(xlsx_file)
    except Exception as e:
        raise ValueError(f"Ошибка при создании XLSX файла: {e}")
```
Что делает функция:
1. Проверяет существование файла
2. Проверяет расширение
3. Читает строки в кодировке UTF-8
3. Создает книгу Excel с помощью openpyxl
4. Добавляет строки CSV в лист Sheets
5. Рассчитывает ширину столбцов
6. Сохраняет результат по указанному пути

Как рассчитывается ширина столбца: 
```python
for i, wid in wid.items():
    ws.column_dimensions[get_column_letter(i)].wid = max(wid, 8)
```
- превращаем номера колонок в буквы
- берем найденную длину и сравниваем, ищем максимум

## Тесты задания В и проверка на совпадение длины
![](/image/lab05/testB_lab05.png)
- создается файл `people_from_csv.xlsx`

## Примеры данных и результаты

- `data/lab05/samples/people.json` — список людей в формате JSON;
- `data/lab05/samples/people.csv` — те же данные в формате CSV;
- `data/lab05/samples/cities.csv` — дополнительный CSV с городами;
- `data/lab05/out/people_from_json.csv` — результат JSON → CSV;
- `data/lab05/out/people_from_csv.json` — результат CSV → JSON;
- `data/lab05/out/people.xlsx` — результат CSV → XLSX.

## Проверка результатов

### 1. JSON -> CSV
![](/image/lab05/json_to_csv.png)

*Рис 1. Результат преобразования JSON в CSV.*

### 2. CSV -> JSON
![](/image/lab05/csv_to_json.png)

*Рис. 2. Результат преобразования CSV в JSON.*

### 3. CSV → XLSX
![](/image/lab05/csv_to_xlsx.png)

*Рис. 3. Результат преобразования CSV в XLSX.*
