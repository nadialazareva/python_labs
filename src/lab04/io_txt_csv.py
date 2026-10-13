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

#-----------------------------------------------------------------------------------------------------------

def ensure_parent_dir(path: str | Path) -> None:
    '''Создаем родительские папки, если их еще нет.
    Args: 
        path: путь к файлу
    Returns:
        None
    '''
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

#-----------------------------------------------------------------------------------------------------------
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

#ПРОВЕРКА ТЕСТ-КЕЙСОВ

if __name__ == "__main__":
    Path("data/lab04/input.txt").write_text("Привет, мир, привет!!!",encoding = "utf-8")
    txt = read_text("data/lab04/input.txt")
    print("Успешно прочитано")
    write_csv([("word","count"),("test",3)], "data/lab04/check.csv")
    print("Файл создан")


