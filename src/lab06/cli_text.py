"ЛР6: подкоманды stats и cat для работы с текстом"

import argparse
import sys
from src.lab04.io_txt_csv import read_text
from lib.text import count_freq, normalize, tokenize, top_n

def stats_cmd(path: str, top: int) -> None:
    '''Напечатать число слов и топ самых частых'''

    tokens = tokenize(normalize(read_text(path)))
    freq = count_freq(tokens)

    print(f"Всего слов: {len(tokens)}")
    print(f"Уникальных слов: {len(freq)}")
    print("Топ-5:")
    for word, count in top_n(freq,top):
        print(f"{word}:{count}")

def cat_cmd(path: str, numbered: bool) -> None:
    '''
    Подкоманда cat: выводит содержимое файла построчно.
    Если указан флаг -n - перед каждой строкой печатается её номер.
    '''
    #splitlines() режет текст на строки (без символов переноса)
    lines = read_text(path).splitlines()

    for number, line in enumerate(lines, start = 1):
        if numbered:
            print(f"{number}:{line}")
        else:
            print(line)

def main() -> None:
    parser = argparse.ArgumentParser(description="Текстовые утилиты: статистика слов и вывод файла")
    sub = parser.add_subparsers(dest="command", required=True)

    #подкоманда stats
    stats_parser = sub.add_parser("stats", help="частоты слов в тексте")
    stats_parser.add_argument("--input", required=True, help="текстовый файл")
    stats_parser.add_argument("--top", type=int, default=5, help="сколько слов показать(по умолчанию 5)")

    #подкоманда cat
    cat_parser = sub.add_parser("cat", help="вывести файл построчно")
    cat_parser.add_argument("--input", required=True, help="файл для вывода")
    cat_parser.add_argument("-n", action="store_true", help="нумеровать строки")

    args = parser.parse_args()

    if args.command == "stats" and args.top < 1:
                parser.error("--top должен быть положительным числом")
    try:
        if args.command == "stats":
            stats_cmd(args.input, args.top)
        elif args.command == "cat":
            cat_cmd(args.input, args.n)
    except FileNotFoundError:
        parser.error(f"файл не найден: {args.input}")
    except UnicodeDecodeError:
         parser.error(f"файл {args.input} не читается в кодировке UTF-8")       

if __name__ == "__main__":
    main()

# python -m src.lab06.cli_text cat --input data/lab05/samples/people.csv -n
# python -m src.lab06.cli_text stats --input data/lab06/samples/people.txt --top 5


