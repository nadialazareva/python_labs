import argparse
import csv
import sys

from src.lab08.models import format_student, make_student
from src.lab09 import group

def main() -> int:
    '''Выполнить команду хранилища студентов'''
    parser = argparse.ArgumentParser(description="Хранилище студентов на CSV")
    parser.add_argument('--db', default='data/lab09/students.csv', help='путь к CSV')
    sub = parser.add_subparsers(dest='command', required=True)

    add = sub.add_parser('add', help='добавить студента')
    add.add_argument('--fio', required=True)
    add.add_argument('--birthdate', required=True)
    add.add_argument('--gpa', required=True)
    add.add_argument('--group', required=True)


    listing = sub.add_parser('list', help='вывести студентов')
    listing.add_argument('--sort', choices=('fio', 'gpa'))

    find = sub.add_parser('find', help='найти по ФИО')
    find.add_argument('--q', required=True)

    remove = sub.add_parser('remove', help='удалить по ФИО')
    remove.add_argument('--fio', required=True)

    update = sub.add_parser('update', help='обновить запись')
    update.add_argument('--fio', required=True)
    update.add_argument('--gpa', type=float)
    update.add_argument('--group')
    update.add_argument('--birthdate')

    args = parser.parse_args()

    try:
        if args.command == 'add':
            student = make_student(args.fio, args.birthdate, args.group, args.gpa)
            group.add_student(args.db, student)
            print('Добавлен:', format_student(student))

        elif args.command == 'list':
            for student in group.list_students(args.db, args.sort):
                print(format_student(student))

        elif args.command == 'find':
            for student in group.find_students(args.db, args.q):
                print(format_student(student))

        elif args.command == 'remove':
            print('Удалено:', group.remove_student(args.db, args.fio))

        elif args.command == 'update':
            # берем только те поля, которые пользователь действительно указал
            fields = {}
            if args.birthdate is not None:
                fields["birthdate"] = args.birthdate
            if args.group is not None:
                fields["group"] = args.group
            if args.gpa is not None:
                fields["gpa"] = args.gpa

            if not fields:
                parser.error("укажите хотя бы одно поле для обновления: --birthdate, --group или --gpa")
    
    except (ValueError, KeyError, OSError, csv.Error) as error:
        print(f'Ошибка: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())

#  python -m src.lab09.cli_students list --sort gpa            
