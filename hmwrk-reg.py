from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re
import itertools


with open('phonebook_raw.csv', encoding='utf8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


# TODO 1: выполните пункты 1-3 ДЗ
# Пункт 1
for item in contacts_list:
    i = 0
    while i <= 3:
        buf = re.split(' ', item[i])
        if len(buf) == 3:  # ФИО
            item[i] = buf[i]
            item[i+1] = buf[i+1]
            item[i+2] = buf[i+2]
        if (len(buf) == 2) and (i != 0):  # Ф + ИО
            item[i] = buf[i-1]
            item[i+1] = buf[i]
        if (len(buf) == 2) and (i == 0):
            item[i] = buf[i]
            item[i+1] = buf[i+1]
        i += 1

# Пункт 2
for item in contacts_list:
    pattern = re.compile('(\+7|8)?[\s]?\(?(\d{3})\)?[\s-]*(\d{3})[-]*(\d{2})[-]*(\d{2})((\,|\s)\(*(доб.)?)+(\d{4})*\)*')
    result = re.sub(pattern, r'+7(\2)\3-\4-\5 \8\9', item[5] + '  ')
    item[5] = result.strip()

# Пункт 3
lastname_list = []
empty_list = [[]]
for item in contacts_list:
    lastname_list.append(item[0])  # получили список фамилий контакт листа
    empty_list.append([])

out_dict = {}
out_dict = dict(zip(lastname_list, empty_list))  # создали словарь чтобы объединить по ключу информацию дублей

i = 0
for item in contacts_list:
    for key in out_dict.keys():
        if item[0] == key:
            out_dict[key].append(item)   # в словаре по ключу с фамилией вся инфа по персоне в виде списка списков

for key in out_dict.keys():
        out_dict[key] = list(itertools.chain.from_iterable(out_dict[key]))  # сделали плоским список с инфой по дублю

out_list = []
for value in out_dict.values():
    out_list.append(value)  # словарь теперь не нужен, работаем снова со списком

for item in out_list:  # первые 7 полей списка заполняются максимально
    for i in range(6):
        if (item[i] == '') and (len(item) > 7):
            item[i] = item[i + 7]


for item in out_list:
    while len(item) != 7:
        item.pop()  # оставшиеся поля в списке не нужны - удаляем

pprint(out_list)


# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open('phonebook.csv', 'w', encoding='utf8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(out_list)