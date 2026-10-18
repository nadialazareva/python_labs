'''ЛР5 задание В: конвертация CSV -> XLSX'''

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

    if not data or len(data)<2:
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

if __name__ == "__main__":
    print("=" * 30)

    in_csv = "data/lab05/samples/people.csv"
    out_xlsx = "data/lab05/out/people_from_csv.xlsx"

    try:
        print("Test 3: CSV -> XLSX ")
        with open(in_csv, 'r', encoding = 'utf-8') as f:
            c_len = len(f.readlines()) -1

        csv_to_xlsx(in_csv, out_xlsx)

        wb = openpyxl.load_workbook(out_xlsx)
        ws = wb["Sheet1"]
        final_xlsx_len = ws.max_row - 1

        print(f"---Zapisi CSV: {c_len}")
        print(f"---Zapisi XLSX: {final_xlsx_len}")

        assert c_len == final_xlsx_len, "Erorr"
        print('='*30)
    except Exception as e:
        print(f"\nErorr: {e}")







