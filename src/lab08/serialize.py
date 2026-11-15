import json
from pathlib import Path
from datetime import date

from src.lab04.io_txt_csv import read_text
from src.lab08.models import(
    STUDENT_FIELDS,
    format_student,
    make_student,
    student_age,
    student_from_dict,
    student_to_dict,
    )

def students_to_json(students: list[dict], path: str | Path) -> None:
    '''Сохраняем студентов в JSON'''
    data = [student_to_dict(student) for student in students]
    with Path(path).open('w', encoding = 'utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def students_from_json(path: str | Path) -> list[dict]:
    '''Загружаем студентов и проверяем каждую запись'''
    with Path(path).open(encoding = 'utf-8') as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError('В JSON ожидается массив студентов')

    students = []
    for number, item in enumerate(data, start=1):
        try:
            student = student_from_dict(item)
        except ValueError:
            raise ValueError(f'Запись {number} некорректна')
        students.append(student)
    return students


if __name__ == "__main__":
    input_file = "data/lab08/samples/students_input.json"
    output_file = "data/lab08/out/students_output.json"
    bad_file = "data/lab08/samples/students_bad.json"

    # Чтение корректного файла и запись в новый
    print(f"1. Чтение из {input_file} и сохранение в {output_file}:")
    try:
        students_list = students_from_json(input_file)
        print(f"Успешно загружено записей: {len(students_list)}")
        students_to_json(students_list, output_file)
    except Exception as e:
        print(f"Ошибка: {e}")

    # Проверка строгой валидации на битом файле
    print(f"2. Попытка загрузить файл с ошибками ({bad_file}):")
    try:
        students_from_json(bad_file)
    except ValueError as e:
        print(f"Ошибка: {e}")

# python -m src.lab08.serialize