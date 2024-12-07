from pprint import pprint
import numpy as np

stuffdict = {'r': (3, 25),
             'p': (2, 15),
             'a': (2, 15),
             'm': (2, 20),
             'i': (1, 5),
             'k': (1, 15),
             'x': (3, 20),
             't': (1, 25),
             'f': (1, 15),
             's': (2, 20),
             'c': (2, 20)} # удалил отсюда обязательный элемент, он и так будет в рюкзаке

we_have_scores = 10
selected_stuff = {'d': {'area': 1, 'price': 10}}

def get_area_and_value(stuffdict):
    area = [stuffdict[item][0] for item in stuffdict]
    value = [stuffdict[item][1] for item in stuffdict]
    return area, value


def get_memtable(stuffdict, A=4*2 - 1):
    area, value = get_area_and_value(stuffdict)
    n = len(value)  # находим размеры таблицы

    # создаём таблицу из нулевых значений
    V = [[0 for a in range(A + 1)] for i in range(n + 1)]

    for i in range(n + 1):
        for a in range(A + 1):
            # базовый случай
            if i == 0 or a == 0:
                V[i][a] = 0

            # если площадь предмета меньше площади столбца,
            # максимизируем значение суммарной ценности
            elif area[i - 1] <= a:
                V[i][a] = max(value[i - 1] + V[i - 1][a - area[i - 1]], V[i - 1][a])

            # если площадь предмета больше площади столбца,
            # забираем значение ячейки из предыдущей строки
            else:
                V[i][a] = V[i - 1][a]
    return V, area, value


def get_selected_items_list(stuffdict, A=4*2 - 1):
    V, area, value = get_memtable(stuffdict)
    n = len(value)
    res = V[n][A]  # начинаем с последнего элемента таблицы
    a = A  # начальная площадь - максимальная
    items_list = []  # список площадей и ценностей

    for i in range(n, 0, -1):  # идём в обратном порядке
        if res <= 0:  # условие прерывания - собрали "рюкзак"
            break
        if res == V[i - 1][a]:  # ничего не делаем, двигаемся дальше
            continue
        else:
            # "забираем" предмет
            items_list.append((area[i - 1], value[i - 1]))
            res -= value[i - 1]  # отнимаем значение ценности от общей
            a -= area[i - 1]  # отнимаем площадь от общей


    # находим ключи исходного словаря - названия предметов
    for search in items_list:
        for key, value in stuffdict.items():
            if value == search and key not in selected_stuff:
                selected_stuff[key] = {'area': value[0], 'price': value[1]}
                break

    return selected_stuff


def normalize(table):
    for i in range(len(table)):
        for j in range(len(table[0])):
            table[i][j] = f"{table[i][j]}".ljust(3, '.')
    return table


our_things_book = get_selected_items_list(stuffdict, A=4*2-1)
ans = [key for key in our_things_book]
for key, el in our_things_book.items():
    while ans.count(key) != el['area']: ans.insert(ans.index(key), key)

inventory = np.array(ans)
print(np.reshape(inventory, (2, 4)))

all_scores = sum(el[1] for el in stuffdict.values())
all_our_scores = all_scores - sum([el[1] for key, el in stuffdict.items() if el not in ans])

print('Scores amount:', all_our_scores + we_have_scores, end='\n\n')

print('Рюкзак из семи предметов:')
seven_things_book = get_selected_items_list(stuffdict, A=4*2-2)
ans = [key for key in seven_things_book]
for key, el in our_things_book.items():
    while ans.count(key) != el['area']: ans.insert(ans.index(key), key)

all_scores = sum(el[1] for el in stuffdict.values())
all_our_scores = all_scores - sum([el[1] for key, el in stuffdict.items() if el not in ans])
print(ans)
print('Scores amount:', all_our_scores + we_have_scores)

