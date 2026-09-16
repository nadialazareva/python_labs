fio = input("ФИО: ").split()
i = ""
for word in fio:
    i = i + word[0].upper()
fio_clean = "".join(fio)
dl = len(fio_clean)+2
print(f"Инициалы:{i}.")
print(f"Длина (символов):{dl}")