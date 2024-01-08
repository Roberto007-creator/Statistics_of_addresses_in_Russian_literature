import os


alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '

official_addresses = dict()
title_addresses = dict()
common_addresses = dict()


# функция для чистки словарей:
def resetting_dictionaries():
    # формирование словаря для официальных обращений: ключ - обращение, значение - встречаемость:
    with open("Этикетные обращения/Официальные обращения.txt", encoding='UTF-8') as file:
        for line in file.readlines():
            official_addresses[line.strip()] = 0

    # формирование словаря для титульных обращений: ключ - обращение, значение - встречаемость:
    with open("Этикетные обращения/Обращения связанные с титулом.txt", encoding='UTF-8') as file:
        for line in file.readlines():
            title_addresses[line.strip()] = 0

    # формирование словаря для принятых в обиходе обращений: ключ - обращение, значение - встречаемость:
    with open("Этикетные обращения/Обращения принятые в обиходе.txt", encoding='UTF-8') as file:
        for line in file.readlines():
            common_addresses[line.strip()] = 0


# основная часть кода, читающая произведения и отбирающая нужные слова:
with open("Статистика обращений.csv", 'w') as out_file:
    resetting_dictionaries()

    # записываем шапку таблицы
    out_file.write(f"Произведение;Автор;Год написания;{';'.join(official_addresses.keys())};"
                   f"{';'.join(common_addresses.keys())};{';'.join(title_addresses.keys())}\n")

    for file_name in os.listdir("Литературные произведения"):
        resetting_dictionaries()
        print(file_name)

        with open(f"Литературные произведения/{file_name}") as in_file:
            for line in in_file.readlines():
                # убираем из строчки лишнее символы
                line = ''.join(filter(lambda x: x.upper() in alphabet, line.strip()))

                # увеличиваем регистр, чтобы программа не учитывала его и работала корректно
                line = line.upper()
                line = line.split()

                # отбираем нужные нам слова по трём группам:
                for key in official_addresses.keys():
                    official_addresses[key] += line.count(key.upper())

                for key in title_addresses.keys():
                    if ' ' in key:
                        line = ' '.join(line)
                        title_addresses[key] += line.count(key.upper())
                        line = line.split()
                    else:
                        title_addresses[key] += line.count(key.upper())

                for key in common_addresses.keys():
                    common_addresses[key] += line.count(key.upper())

        out_file.write(f"{file_name.split('. ')[0]};{file_name.split('. ')[1]};{file_name.split('. ')[2][:4]};"
                       f"{';'.join(map(str, official_addresses.values()))};"
                       f"{';'.join(map(str, common_addresses.values()))};"
                       f"{';'.join(map(str, title_addresses.values()))}\n")


# Пока что всё :)
