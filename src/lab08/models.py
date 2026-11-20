from datetime import date

STUDENT_FIELDS = ("fio", "birthdate", "group", "gpa") # эталон

def validate_student(rec: dict) -> None:
    if not isinstance(rec, dict):
        raise ValueError('student должен быть словарем')
    
    if set(rec) != set(STUDENT_FIELDS):
        raise ValueError('нужны только поля fio, birthdate, group, gpa')

    for field in ('fio', 'group'):
        value = rec[field]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f'{field}: нужна непустая строка')
        
    birthdate = rec['birthdate']
    if not isinstance(birthdate, str):
        raise ValueError('birthdate требует формат YYYY-MM-DD')
    try:
        birthday = date.fromisoformat(birthdate) #преобразовываем строку в объект даты
    except ValueError:
        raise ValueError('birthdate: неверная дата или формат')

    if birthday.isoformat() != birthdate: #проверка на строгий формат(добавляем недостающие нули)
        raise ValueError('нужен формат YYYY-MM-DD')

    if birthday > date.today():
        raise ValueError('birthdate: дата рождения не может быть в будущем')

    gpa = rec['gpa']
    if isinstance(gpa, bool) or not isinstance(gpa, (int, float)):
        raise ValueError('GPA должен быть числом (float или int)')
    if not (0 <= gpa <= 5):
        raise ValueError('gpa: требуется значение от 0 до 5')

def make_student(fio, birthdate, group, gpa) -> dict:
    '''Создаем проверенную запись студента'''
    rec = {"fio": fio, "birthdate": birthdate, "group": group, "gpa": gpa}
    validate_student(rec)
    rec['fio'] = fio.strip()
    rec['group'] = group.strip()
    rec['gpa'] = float(gpa)
    return rec

def student_age(rec: dict, today: date | None=None) -> int:
    '''Считаем полные годы на указанную дату'''
    if today is None:
        today = date.today()
    birthday = date.fromisoformat(rec["birthdate"]) #превращаем строку даты рожд. в объект даты
    age = today.year - birthday.year
    if (today.month, today.day) < (birthday.month, birthday.day):
        age-=1
    return age

def format_student(rec: dict) -> str:
    '''Форматируем запись студента в читаемую строку с инициалами и возрастом'''
    validate_student(rec)

    fio_parts = rec['fio'].split()
    surname = fio_parts[0].capitalize()
    initials = "".join(f"{part[0].upper()}." for part in fio_parts[1:])

    age = student_age(rec)
    return f"{surname} {initials} ({rec['group']}), {age} лет, GPA {rec['gpa']}"

def student_to_dict(rec: dict) -> dict:
    '''Возвращаем копию записи для сериализации'''
    validate_student(rec)
    return rec.copy()

def student_from_dict(d: dict) -> dict:
    '''Десериализует словарь, приводит типы и проверяет запись через валидацию'''
    if not isinstance(d, dict):
        raise ValueError('Ожидался словарь для десериализации студента')

    fio = d.get('fio')
    birthdate = d.get('birthdate')
    group = d.get('group')
    gpa = d.get('gpa')

    if gpa is not None and not isinstance(gpa, bool):
        try:
            gpa = float(gpa)
        except (ValueError, TypeError):
            pass

    rec = {"fio": fio, "birthdate": birthdate, "group": group, "gpa": gpa}
    validate_student(rec)
    return rec

if __name__ == "__main__":

    student = make_student("Иванов Иван Иванович", "2008-04-30", "БИВТ-26-6-1", 4.3)
    print("Создан студент:", student)

    print("Форматирование:", format_student(student))

    print("Возраст:", student_age(student))

    print("Попытка создать студента с GPA = 9:")
    try:
        make_student("Петров Петр", "2008-04-01", "БИВТ-26-6-1", 9.0)
    except ValueError as e:
        print(f"Перехвачена ошибка: {e}")

          
        