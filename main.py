import os
import pymorphy2


alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '
morphy = pymorphy2.MorphAnalyzer()


# формирование словаря для официальных обращений: ключ - обращение, значение - встречаемость:
official_addresses = dict()
with open("Этикетные обращения/Официальные обращения.txt", encoding='UTF-8') as file:
    for line in file.readlines():
        official_addresses[line.strip()] = 0

# формирование словаря для титульных обращений: ключ - обращение, значение - встречаемость:
title_addresses = dict()
with open("Этикетные обращения/Обращения связанные с титулом.txt", encoding='UTF-8') as file:
    for line in file.readlines():
        title_addresses[line.strip()] = 0

# формирование словаря для принятых в обиходе обращений: ключ - обращение, значение - встречаемость:
common_addresses = dict()
with open("Этикетные обращения/Обращения принятые в обиходе.txt", encoding='UTF-8') as file:
    for line in file.readlines():
        common_addresses[line.strip()] = 0


# основная часть кода, читающая произведения и отбирающая нужные слова:
for file_name in os.listdir("Литературные произведения"):
    with open(f"Литературные произведения/{file_name}") as in_file,\
            open(f"Статистика обращений/Статистика_{file_name[:file_name.rfind('.')]}.csv", 'w') as out_file:
        for line in in_file.readlines():
            # убираем из строчки лишнее символы
            line = ''.join(filter(lambda x: x.upper() in alphabet, line.strip()))

            # оставляем только сущестивительные в строчке
            line = ' '.join(filter(lambda x: any(map(lambda p: p.tag.POS == 'NOUN', morphy.parse(x))), line.split()))

            # увеличиваем регистр, чтобы программа не учитывала его и работала корректно
            line = line.upper()

            # отбираем нужные нам слова по трём группам:
            for key in official_addresses.keys():
                official_addresses[key] += line.count(key.upper())

            for key in title_addresses.keys():
                title_addresses[key] += line.count(key.upper())

            for key in common_addresses.keys():
                common_addresses[key] += line.count(key.upper())

        # запись результата в файл:
        out_file.write("Официальные обращения:;Встречаемость:\n")
        for key, value in official_addresses.items():
            out_file.write(f'{key};{value}\n')
        out_file.write('\n\n')

        out_file.write("Обращения принятые в обиходе:;Встречаемость:\n")
        for key, value in common_addresses.items():
            out_file.write(f'{key};{value}\n')
        out_file.write('\n\n')

        out_file.write("Титульные обращения:;Встречаемость:\n")
        for key, value in title_addresses.items():
            out_file.write(f'{key};{value}\n')


# Пока что всё :)
