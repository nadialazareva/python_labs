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