import csv
from pathlib import Path

from src.lab08.models import (
    STUDENT_FIELDS,
    student_from_dict,
    validate_student,
    )

HEADER = STUDENT_FIELDS

def ensure_storage(path: str | Path) -> None:
    '''Создаем CSV с заголовком, если файла нет'''
    path = Path(path)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok = True)
        with path.open('w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=HEADER)
            writer.writeheader()


def load_students(path: str | Path) -> list[dict]:
    '''Читаем и проверяем всех студентов из файла
    (прочитать весь файл и вернуть список студентов)
    '''
    ensure_storage(path)
    students = []
    with Path(path).open('r', encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != list(HEADER):
            raise ValueError('CSV: нужен заголовок fio, birthdate, group, gpa')
        for number, item in enumerate(reader, start=1): # дает нам номер строки при ошибке
            try:
                student = student_from_dict(item)
            except ValueError as error:
                raise ValueError(f'Запись {number}: {error}') from error
            students.append(student)
    return students


def save_students(path: str | Path, students: list[dict]) -> None:
    '''Перезаписываем CSV с проверенными записями
    (сохранить измененный список студентов обратно в файл)
    '''
    for student in students:
        validate_student(student)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True) #создаем папки, если их нет
    with path.open('w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(students)



def add_student(path: str | Path, student: dict) -> None:
    '''Добавляем студента без дубликатов по ФИО'''
    validate_student(student)
    students = load_students(path)
    for existing in students: #перебор по существующим студентам
        if existing['fio'] == student['fio']:
            raise ValueError('Студент с таким ФИО уже существует')
    students.append(student)
    save_students(path, students)



def list_students(path: str | Path, sort_by: str | None=None) -> list[dict]:
    '''Вернуть список студентов с необязательной сортировкой'''
    if sort_by not in (None, 'fio', 'gpa'):
        raise ValueError('sort_by: допустимы fio, gpa, None')
    students = load_students(path)
    if sort_by is not None:
        students = sorted(students, key=lambda student: student[sort_by]) #сортируем список и указываем, по какому ключу сортировать
    return students


def find_students(path: str | Path, substr: str) -> list[dict]:
    '''Найти по подстроке ФИО без учета регистра'''
    students = load_students(path)
    nizh = substr.casefold() # переводим искомую строку в нижний регистр
    return [student for student in students if nizh in student['fio'].casefold()] #возвращаем список студентов с нужным текстом в ФИО


def remove_student(path: str | Path, fio: str) -> int:
    '''Удалить все записи с указанным ФИО, вернуть количество удалений'''
    students = load_students(path)
    remaining = [student for student in students if student['fio'] != fio] #новый список тех, чье фио НЕ СОВПАДАЕТ с удаляемым
    removed = len(students)-len(remaining) #сколько записей было удалено
    if removed:
        save_students(path, remaining) #новый список без удаленных
    return removed


def update_student(path: str | Path, fio: str, **fields) -> bool:
    '''Обновить первую запись с указанным ФИО
    - результат валидируется
    - возвращает True, если запись найдена и обновлена, иначе False.
    '''
    for field in fields:
        if field not in HEADER:
            raise KeyError(field)
    students = load_students(path)
    for i, student in enumerate(students):
        if student['fio'] == fio:
            updated = dict(student)
            updated.update(fields)
            validate_student(updated)

            students[i] = updated
            save_students(path, students)
            return True
    return False

