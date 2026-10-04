# python_labs

# Лабораторная работа 3

## Задание 1.1

```python
def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    if yo2e:
        text = text.replace('ё', 'е').replace('Ё', 'Е')

    if casefold:
        text = text.casefold()
    else:
        text = text.lower()
    return ' '.join(text.split())
```
Вызываем функцию. Сразу заменяем все буквы Ё на Е и ё на е. Делаем буквы строчными. Разбиваем строку по любым пробельным символам, split() возвращаем список слов, игнорируя множественные пробелы. далее берем список слов и склеиваем их в одну строку, вставляя один пробел.
![Картинка 1](./image/ЛР3/image1.1_lab03.png)

## Задание 1.2

```python
def tokenize(text: str) -> list[str]:
    return re.findall(r'\w+(?:-\w+)*', text)
```
Вызываем функцию. С помощью регулярной строки ищем любые буквенные символы(\w) один или несколько раз(+), символ дефиса, и снова любые буквенные символы один или несколько раз, выражение в скобках может быть ноль или более раз(*).
![Картинка 2](./image/ЛР3/image1.2_lab03.png)

## Задание 1.3 и 1.4

```python
def count_freq(tokens: list[str]) -> dict[str, int]:
    freq = {}
    for token in tokens:
        freq[token] = freq.get(token, 0) + 1
    return freq
```
```python
def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    if n < 0:
        raise ValueError
    return sorted(freq.items(), key = lambda x: (-x[1], x[0]))[:n]
```
Вызываем функцию подсчета токенов. Добавляем переменную множество, в которой будет словарь. Перебираем данный список строк. Метод get() пытается получить значение по ключу token. Если такого ключа в словаре еще нет, он возвращает 0, а если есть - он возвращает текущее число. Прибавляем 1 к этому значению. 
Вызываем функцию вывода самых популярных слов. По умолчанию возвращаем число 5(сколько топ-слов вернуть).Превращаем словарь в список пар(кортежей) и сортируем его. Лямбда-функция юерет x как одну пару. Берем второй элемент пары с минусом. Так как мы сортируем по возрастанию, минус переворачивает порядок: чем больше было число, тем меньше оно станет с минусом, и тем раньше в списке окажется. Срез по n.
![Картинка 3](./image/ЛР3/image1.3_lab03.png)

## Задание 2

```python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib.text import normalize, tokenize, count_freq, top_n

def main():
    text = sys.stdin.read()
    normalized_text = normalize(text)
    tokens = tokenize(normalized_text)
    total_words = len(tokens)
    freq = count_freq(tokens)
    unique_words = len(freq)
    top5 = top_n(freq, 5)
    print(f"Всего слов: {total_words}")
    print(f"Уникальных слов: {unique_words}")
    print(f"Топ-5:")
    for word, count in top5:
        print(f"{word}:{count}")
if __name__ == "__main__":
    main()
```
Подключаем системные модули для работы с путями. ".." означает подняться на одну папку вверх. Программа читает весь текст, введенный в терминал, пока не нажму Ctrl+Z, сохраняем в переменную. Нормализуем текст, разбиваем на отдельные слова, считаем обшее количество слов. Подсчитываем, сколько раз встречается каждое слово, считаем количество уникальных слов, берем 5 самых популярных слов. 
![Картинка 4](./image/lab03/image2_lab03.png)





