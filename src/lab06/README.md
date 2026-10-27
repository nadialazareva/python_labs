# ЛР6 - CLI-утилиты с argparse (cat/grep-lite + конвертеры)

## Задание А: текстовые утилиты (`cli_text.py`)

### Что делает программа:
### Утилиты:
#### 1. cli_text
- stats --> `stats --input <путь> [--top N]` (считает слова, выводит Топ-N)
- cat --> `cat --input <путь> [-n]`(выводит файл построчно, `-n` нумерует строки)
#### 2. cli_convert
- json2csv --> --in, --out (JSON -> CSV)
- csv2json --> --in, --out (CSV -> JSON)
- csv2xlsx -->--in, --out (CSV -> XLSX)

>- С помощью `add.subparsers` создаются подкоманды (`stats`, `cat`, `json2csv` и др.)
>- `dest` служит для того, чтобы переименовать переменную, которую argparse придумал автоматически
>- выбранная команда лежит в args.command

```python
def stats_cmd(path: str, top: int) -> None:
    '''Напечатать число слов и топ самых частых'''

    tokens = tokenize(normalize(read_text(path)))
    freq = count_freq(tokens)

    print(f"Всего слов: {len(tokens)}")
    print(f"Уникальных слов: {len(freq)}")
    print("Топ-5:")
    for word, count in top_n(freq,top):
        print(f"{word}:{count}")
```
```python
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
```
### Выводы:

```
python -m src.lab06.cli_text cat --input data/lab05/samples/people.csv -n
1:name,age,city
2:Alice,22,SPB
3:Bob,25,Moscow
4:Carlos,30,Kazan
5:Dana,21,SPB
6:Andrey,27,Novosibirsk
```
```
Привет, всем! Это моя лабораторная работа по программированию.
Python - это по-настоящему простой язык программирования.
Я надеюсь мне поставят хороший балл за это!
Ёжики живут в лесу
```
```
python -m src.lab06.cli_text stats --input data/lab06/samples/people.txt --top 5
Всего слов: 26
Уникальных слов: 24
Топ-5:
это:3
python:1
балл:1
в:1
всем:1
```
![](/image/lab06/text1_lab06.png)

![](/image/lab06/test2_lab06.png)

## Задание В: Конвертеры (`cli_convert.py`)

Модуль создает утилиту с тремя подкомандами: `json2csv`, `csv2json`, `csv2xslx`. Подкоманды вызывают функции из ЛР5(`json_to_csv`, `csv_to_json`, `csv_to_xlsx`). Обязательно вводить `--in`(входной файл) и `out`(выходной файл).
![](/image/lab06/test3_lab06.png)

```
python -m src.lab06.cli_convert json2csv --in data/lab05/samples/people.json --out data/lab05/out/people.csv
python -m src.lab06.cli_convert csv2json --in data/lab05/samples/people.csv --out data/lab05/out/people.json
python -m src.lab06.cli_convert csv2xlsx --in data/lab05/samples/people.csv --out data/lab05/out/people.xlsx
```
## Справка --help
Это инструкция по эксплуатации программы, которая генерируется автоматически
![](/image/lab06/test4_lab06.png)