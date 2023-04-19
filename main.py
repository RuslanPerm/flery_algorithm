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
    neighbours_of_start_vertex = graph_structure.get(start_vertex)  # берём список соседей начальной вершины

    # составляем словарь соседей соседей начальной точки
    finish_vertex = random.choice(neighbours_of_start_vertex)  # выбираем случайного соседа
    for n_v in neighbours_of_start_vertex:

        if n_v != start:  # условие, что если есть непройденные вершины помимо стартовой, то выбираем её
            finish_vertex = n_v

    neighbours_of_finish_vertex = graph_structure.get(finish_vertex)  # берём список соседей конечной вершины
    neighbours_of_start_vertex.remove(finish_vertex)  # удаляем конечную вершину из соседей начальной вершины
    neighbours_of_finish_vertex.remove(start_vertex)  # удаляем начальную вершину из соседей конечной вершины

    # обновляем граф, учитывая удалённое ребро
    graph_structure.update({start_vertex: neighbours_of_start_vertex})
    graph_structure.update({finish_vertex: neighbours_of_finish_vertex})

    print(f'Из {start_vertex} в {finish_vertex}')

    return graph_structure, finish_vertex


def built_circle(base_graph):
    global start
    if base_graph[0] == 'eiler':  # если граф эйлеровый
        lst_v = [i for i in base_graph[1].keys()]  # составляем список вершин
        start = random.choice(lst_v)  # выбираем случайную вершину
        graph = base_graph[1]  # для удобства работы создаём словарь граф, с которым в последствие и будем работать
        graph, current_vertex = step(start, graph)  # проходим одну итерацию по графу
        way_v = [start, current_vertex]  # создаём список, куда последовательно будем добавлять пройденные вершины

        while current_vertex != start:
            graph, current_vertex = step(current_vertex, graph)
            way_v.append(current_vertex)
        return 'Граф является эйлеровым, вот его маршрут: ', way_v

    elif base_graph[0] == 'semi-eiler':  # если граф полуэйлеровый
        pass
    else:
        return 'Граф не является Эйлеровым, невозможно использовать алгоритм Флери'


def built_way(base_graph):
    pass


# Если Вы хотите ввести свой граф, уберите # у следующей строки и закомментируйте пример
l_v = graph_creation()

# эйлеров граф (пример)
a, b, c, d, e, f = 'a', 'b', 'c', 'd', 'e', 'f'
# l_v = {
#     a: [b, c],
#     b: [a, c, d, e],
#     c: [b, f, d, a],
#     d: [b, e, c, f],
#     e: [b, d],
#     f: [c, d]
# }

is_graph_e = check_e_condition(l_v)
print(l_v)
print(built_circle(is_graph_e))
print(built_way(is_graph_e))

