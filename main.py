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
    not_odd_vertex_lst = []

    for vertex in vertex_list:
        if len(vertex) % 2 == 0:  # если длинна списка вершин, связанных с рассматриваемой чётная
            link_count += 1
        else:
            # если список связанных вершин нечётный, то добавляем в список нечётных вершин
            for key in link_vertex.keys():
                if link_vertex[key] == vertex:
                    not_odd_vertex_lst.append(key)
                    break

    if link_count == len(vertex_list):  # все ли вершины чётные
        return ['eiler', link_vertex]  # возвращаем тип графа, сам граф
    elif len(vertex_list) - link_count >= 2:  # если кол-во вершин с нечётной степенью меньше или равно 2
        # возвращаем тип графа, сам граф, и нечётные вершины, что бы с них начать
        return ['semi-eiler', link_vertex, not_odd_vertex_lst]
    else:
        return 'not eiler'


def dfs(v, g_f):
    n_of_v = g_f.get(v)  # берём соседей планируемой точки
    for i in n_of_v:  # смотрим на них
        count_neighbours = len(g_f.get(i))
        # print(i, g_f.get(i))
        if count_neighbours > 1:  # если хоть у одного соседа планируемой точки больше 1 соседа, то идём в неё
            return v
    return 0


def step(start_vertex, graph_structure, linked_vertexes):  # проходим по ребру, после удаляем его
    # print("start", start_vertex)
    # берём список соседей начальной вершины
    neighbours_of_start_vertex = graph_structure.get(start_vertex)
    # print('start neighbours', neighbours_of_start_vertex)

    finish_vertex = random.choice(neighbours_of_start_vertex)
    # берём список соседей конечной вершины
    neighbours_of_finish_vertex = graph_structure.get(finish_vertex)
    # print('finish neighbours', neighbours_of_finish_vertex)

    # если конечная вершина не единственный сосед (в случае цикла) или это мост, то заново выбираем конечную точку
    if ((is_graph_e[0] == 'eiler') and (len(neighbours_of_finish_vertex) == 1) and (alive_edge_count(linked_vertexes) > 1)) or ((is_graph_e[0] == 'eiler') and (finish_vertex == start_circle) and (len(neighbours_of_start_vertex) > 1)):
        step(start_vertex, graph_structure, linked_vertexes)

    # если планируемая вершина не нечётная вершина, при условии, что она не конечная
    # elif (is_graph_e[0] == 'semi-eiler') and (finish_vertex in is_graph_e[2]) and alive_edge_count(linked_vertexes) > 1:
    #     step(start_vertex, graph_structure, linked_vertexes)

    # если не мост, то идём
    elif dfs(finish_vertex, graph_structure) or (alive_edge_count(linked_vertexes) <= 2):
        # удаляем конечную вершину из соседей начальной вершины
        neighbours_of_start_vertex.remove(finish_vertex)
        # удаляем начальную вершину из соседей конечной вершины
        neighbours_of_finish_vertex.remove(start_vertex)

        # обновляем граф, учитывая удалённое ребро
        graph_structure.update({start_vertex: neighbours_of_start_vertex})
        graph_structure.update({finish_vertex: neighbours_of_finish_vertex})

        # print(f'Из {start_vertex} в {finish_vertex}')

    else:
        step(start_vertex, graph_structure, linked_vertexes)

    return graph_structure, finish_vertex


# считаем количество оставшихся рёбер
def alive_edge_count(linked_vertexes):
    e_c = 0
    for key in linked_vertexes.keys():
        if linked_vertexes[key]:
            e_c += 1
            # print("edges: ", key, linked_vertexes[key])
    return e_c/2


def built_circle(base_graph):
    global start_circle
    lst_v = [i for i in base_graph[1].keys()]  # составляем список вершин
    start_circle = random.choice(lst_v)  # выбираем случайную вершину
    graph = base_graph[1].copy()  # для удобства работы создаём словарь граф, с которым и будем работать
    edge_count = alive_edge_count(l_v)

    graph, current_vertex = step(start_circle, graph, l_v)  # проходим одну итерацию по графу
    circl_v = [start_circle, current_vertex]  # создаём список, куда последовательно будем добавлять пройденные вершины

    while edge_count > 0:
        graph, current_vertex = step(current_vertex, graph, l_v)
        circl_v.append(current_vertex)
        edge_count = alive_edge_count(l_v)
        # print(edge_count)
    return 'Граф является эйлеровым, вот его маршрут: ', circl_v


def built_way(base_graph):
    global start_path
    start_path = random.choice(base_graph[2])  # выбираем случайную из нечётных вершин
    # print(base_graph[2])
    graph = base_graph[1].copy()  # для удобства работы создаём словарь граф, с которым и будем работать
    edge_count = alive_edge_count(l_v_1)

    graph, current_vertex = step(start_path, graph, l_v_1)  # проходим одну итерацию по графу
    way_v = [start_path, current_vertex]  # создаём список, куда последовательно будем добавлять пройденные вершины

    while edge_count > 0:
        graph, current_vertex = step(current_vertex, graph, l_v_1)
        way_v.append(current_vertex)
        edge_count = alive_edge_count(l_v_1)
        # print(edge_count)

    return 'Граф является полуэйлеровым, вот его маршрут: ', way_v


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

# эйлеров путь (пример)
a, b, c, d, e, f = 'a', 'b', 'c', 'd', 'e', 'f'
l_v_1 = {
    a: [b, c],
    b: [a, c, d, e],
    c: [b, f, d, a],
    d: [b, e, c, f],
    e: [b, d, f],
    f: [c, d, e]
}

is_graph_e = check_e_condition(l_v_1)
# print(l_v)
if is_graph_e[0] == 'eiler':  # если граф эйлеровый:
    print(*built_circle(is_graph_e))
elif is_graph_e[0] == 'semi-eiler':  # если граф полуэйлеровый
    print(*built_way(is_graph_e))
else:
    print('Граф не является Эйлеровым, невозможно использовать алгоритм Флёри')


