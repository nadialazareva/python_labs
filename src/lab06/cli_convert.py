"""ЛР6: подкоманды json2csv, csv2json, csv2xlsx"""

import argparse
from src.lab05.csv_xlsx import csv_to_xlsx
from src.lab05.json_csv import json_to_csv, csv_to_json

def main() -> None:
    parser = argparse.ArgumentParser(description="Конвертеры данных между JSON, CSV и XLSX")
    sub = parser.add_subparsers(dest="command", required=True)

    # dest нужен, чтобы флаг --in сохранялся как input. in зарезервирован в Python.
    json2csv_parser = sub.add_parser("json2csv", help="JSON -> CSV")
    json2csv_parser.add_argument("--in", dest="input", required=True, help="входной JSON")
    json2csv_parser.add_argument("--out", dest="output", required=True, help="выходной JSON")

    csv2json_parser = sub.add_parser("csv2json", help="CSV -> JSON")
    csv2json_parser.add_argument("--in", dest="input", required=True, help="входной CSV")
    csv2json_parser.add_argument("--out", dest="output", required=True, help="выходной CSV")

    csv2xlsx_parser = sub.add_parser("csv2xlsx", help="CSV -> XLSX")
    csv2xlsx_parser.add_argument("--in", dest="input", required=True, help="входной CSV")
    csv2xlsx_parser.add_argument("--out", dest="output", required=True, help="выходной XLSX")

    args = parser.parse_args()

    try:
        if args.command == "json2csv":
            json_to_csv(args.input, args.output)
        elif args.command == "csv2json":
            csv_to_json(args.input, args.output)
    except FileNotFoundError:
        parser.error(f"Ошибка: файл не найден: {args.input}")
    except ValueError as e:
        parser.error(str(e))

    print(f"Готово: {args.input} -> {args.output}")

if __name__ == "__main__":
    main()

# python -m src.lab06.cli_convert json2csv --in data/lab05/samples/people.json --out data/lab05/out/people.csv
# python -m src.lab06.cli_convert csv2json --in data/lab05/samples/people.csv --out data/lab05/out/people.json
# python -m src.lab06.cli_convert csv2xlsx --in data/lab05/samples/people.csv --out data/lab05/out/people.xlsx
