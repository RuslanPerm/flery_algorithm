# создание графа
def graph_creation():
    try:
        vertex_quantity = int(input('Введите кол-во вершин: '))
        l_v = {}  # создаём будущий граф

        # составляем граф, создавая по 1 вершине и прикрепляя к ней связаннные вершины в виде списка
        for vertex in range(vertex_quantity):
            v_name = input('Введите название вершины: ')
            linked_vertex_quantity = int(input('Со сколькими вершинами она связана: '))
            linked_vertex_list = []

            for v in range(linked_vertex_quantity):
                linked_vertex_list.append(input(f'Введите название вершины, связанной с {v_name}: '))

            l_v.update({v_name: linked_vertex_list})

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
        return 'eiler'
    elif len(vertex_list) - link_count >= 2:  # если кол-во вершин с нечётной степенью меньше или равно 2
        return 'semi-eiler'


# эйлеров граф (пример)
# a, b, c, d, e, f = '1', '2', '3', '4', '5', '6'
# l_v = {
#     a: [b, c],
#     b: [a, c, d, e],
#     c: [b, f, d, a],
#     d: [b, e, c, f],
#     e: [b, d],
#     f: [c, d]
# }

# check_e_condition(l_v)
check_e_condition(graph_creation())
