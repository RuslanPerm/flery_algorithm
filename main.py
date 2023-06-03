import random


# создание графа
def graph_creation():
    try:
        vertex_quantity = int(input('Введите кол-во вершин: '))
        l_v = {}  # создаём будущий граф

        # составляем граф, создавая по 1 вершине и прикрепляя к ней связаннные вершины в виде списка
        for vertex in range(vertex_quantity):
            v_name = input('Введите название вершины: ')
            linked_vertex_list = input(f'Введите название вершин, связанных с {v_name} (через пробел): ').split()

            l_v.update({v_name: linked_vertex_list})  # добавляем в словарь к ключу вершины список из связанных вершин

        return l_v

    except ValueError or TypeError:
        print('Введите целое число вершин, попробуйте ещё раз')
        graph_creation()


# проверка на условие эйлеровости
def check_e_condition(link_vertex):
    link_count = 0  # количество чётных связей вершины
    vertex_list = link_vertex.values()  # список вершин

    for vertex in vertex_list:
        if len(vertex) % 2 == 0:  # если длинна списка вершин, связанных с рассматриваемой чётная
            link_count += 1

    if link_count == len(vertex_list):  # все ли вершины чётные
        return ['eiler', link_vertex]  # возвращаем тип графа, сам граф
    elif len(vertex_list) - link_count >= 2:  # если кол-во вершин с нечётной степенью меньше или равно 2
        return ['semi-eiler', link_vertex]  # возвращаем тип графа, сам граф
    else:
        return 'not eiler'


def step(start_vertex, graph_structure):  # проходим по ребру, после удаляем его
    # print("start", start_vertex)

    # берём список соседей начальной вершины
    neighbours_of_start_vertex = graph_structure.get(start_vertex)
    # print('start neighbours', neighbours_of_start_vertex)

    finish_vertex = random.choice(neighbours_of_start_vertex)
    # берём список соседей конечной вершины
    neighbours_of_finish_vertex = graph_structure.get(finish_vertex)
    # print('finish neighbours', neighbours_of_finish_vertex)

    # если конечная вершина не единственный сосед или это мост, то заново выбираем конечную точку
    if ((finish_vertex == start) and (len(neighbours_of_start_vertex) > 1)) or \
            ((len(neighbours_of_finish_vertex) == 1) and (alive_egde_count() > 1)):
        step(start_vertex, graph_structure)
    else:
        # if len(neighbours_of_finish_vertex) > 0 and (alive_egde_count() > 0):
            # if finish_vertex:
        # удаляем конечную вершину из соседей начальной вершины
        neighbours_of_start_vertex.remove(finish_vertex)
        # удаляем начальную вершину из соседей конечной вершины
        neighbours_of_finish_vertex.remove(start_vertex)

        # обновляем граф, учитывая удалённое ребро
        graph_structure.update({start_vertex: neighbours_of_start_vertex})
        graph_structure.update({finish_vertex: neighbours_of_finish_vertex})

        print(f'Из {start_vertex} в {finish_vertex}')

        # else:
        #     print("Осталась конечная вершина, ", finish_vertex)
    print(start_vertex)
    print(finish_vertex)
    return graph_structure, finish_vertex


# считаем количество оставшихся рёбер
def alive_egde_count():
    e_c = 0
    for key in l_v.keys():
        if l_v[key]:
            e_c += 1
            # print("edges: ", key, l_v[key])
    return e_c//2


def built_circle(base_graph):
    global start
    lst_v = [i for i in base_graph[1].keys()]  # составляем список вершин
    start = random.choice(lst_v)  # выбираем случайную вершину
    # start = c
    graph = base_graph[1].copy()  # для удобства работы создаём словарь граф, с которым и будем работать
    graph, current_vertex = step(start, graph)  # проходим одну итерацию по графу
    way_v = [start, current_vertex]  # создаём список, куда последовательно будем добавлять пройденные вершины

    edge_count = alive_egde_count()
    while edge_count > 0:
        graph, current_vertex = step(current_vertex, graph)
        way_v.append(current_vertex)
        edge_count = alive_egde_count()
        # print(edge_count)
    return 'Граф является эйлеровым, вот его маршрут: ', way_v


def built_way(base_graph):
    pass


# Если Вы хотите ввести свой граф, уберите # у следующей строки и закомментируйте пример
# l_v = graph_creation()

# эйлеров граф (пример)
a, b, c, d, e, f = 'a', 'b', 'c', 'd', 'e', 'f'
l_v = {
    a: [b, c],
    b: [a, c, d, e],
    c: [b, f, d, a],
    d: [b, e, c, f],
    e: [b, d],
    f: [c, d]
}

is_graph_e = check_e_condition(l_v)
# print(l_v)
if is_graph_e[0] == 'eiler':  # если граф эйлеровый:
    print(*built_circle(is_graph_e))
elif is_graph_e[0] == 'semi-eiler':  # если граф полуэйлеровый
    print(built_way(is_graph_e))
else:
    print('Граф не является Эйлеровым, невозможно использовать алгоритм Флёри')


