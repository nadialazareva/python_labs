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
            reader = csv.DictResder(f)
        if reader.fieldnames is None:
            raise ValueError('CSV-файл пуст или нет заголовка')
        data = list(reader)
        if not data:
            raise ValueError('CSV-файл не содержит данных(только заголовок)')
        
    except csv.Error as e:
        raise ValueError(f"Ощибка чтения CSV")
    
    try:
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
