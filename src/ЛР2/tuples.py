def format_record(rec: tuple[str, str, float]) -> str:
    if not isinstance(rec,tuple):
        raise TypeError
    fio, group, gpa = rec
    if not isinstance(fio,str) or not isinstance(group, str):
        raise TypeError
    if not isinstance(gpa, (int, float)):
        raise TypeError
    fio_parts = fio.strip().split()
    if not fio_parts:
        raise TypeError
    surname = fio_parts[0]
    surname = surname[0].upper()+surname[1:].lower()
    initials = ''.join([part[0].upper() + '.' for part in fio_parts[1:]])
    formatted_fio = f'{surname} {initials}'.strip()
    formatted_group = group.strip()
    if not formatted_group:
        raise ValueError
    if gpa<0 or gpa>5:
        raise ValueError
    formatted_gpa = f'{gpa:.2f}'
    return f'{formatted_fio}, гр. {formatted_group}, GPA {formatted_gpa}'
print(format_record(('Иванов Иван Иванович', 'BIVT-25', 4.6)))
print(format_record(('Петров Пётр', 'IKBO-25', 5.0)))
print(format_record(('Петров Пётр Петрович', 'IKBO-12', 5.0)))
print(format_record(('  сидорова  анна  сергеевна', 'ABB-01', 3.999)))
