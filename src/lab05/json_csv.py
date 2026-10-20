''' ЛР5 задание А: конвертация JSON <-> CSV'''

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

if __name__ == "__main__":
    sample_json = "data/lab05/samples/people.json"
    out_csv = "data/lab05/out/people_from_json.csv"
    out_json = "data/lab05/out/people_from_csv.json"

    print("="*30)

    try:
        #----------------------------------
        # JSON -> CSV
        #----------------------------------
        print('Test1: JSON -> CSV')
        with open(sample_json, 'r', encoding = 'utf-8') as f:
            j_len = len(json.load(f))
        json_to_csv(sample_json,out_csv)

        with open(out_csv, 'r', encoding = 'utf-8') as f:
            c_len = len(f.readlines()) -1 #тк не считаем заголовок
        print(f"---Zapisi JSON: {j_len}")
        print(f"---Zapisi CSV: {c_len}")

        assert j_len == c_len, 'Error'

        print('-'*30)
        #-------------------------------------
        # CSV -> JSON
        #-------------------------------------

        print('Test2: CSV -> JSON')
        csv_to_json(out_csv, out_json)
        with open(out_json, 'r', encoding = 'utf-8') as f:
            final_j_len = len(json.load(f))
        print(f"---Zapisi CSV: {c_len}")
        print(f"---Zapisi JSON: {final_j_len}")

        assert c_len == final_j_len, 'Error'

        print('='*30)
    except Exception as e:
        print(f"\nOh no! Erorr: {e}")



    
    

    

    