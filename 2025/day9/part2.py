# %%
from itertools import combinations, product
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

######################
#### Initialise ######
######################


def get_content(use_demo: bool):
    print("*" * 50, "Import Data", "*" * 50)
    if use_demo:
        file = Path("input_example.txt")
    else:
        file = Path("input.txt")

    with open(file) as f:
        content: str = f.read()
    content_list: list[str] = content.split("\n")
    content_list = content_list[:-1]
    parsed_liste = []
    for x in content_list:
        split = x.split(",")
        temporary_tuple = (int(split[0]), int(split[1]))
        parsed_liste.append(temporary_tuple)
    return parsed_liste


liste = get_content(use_demo=False)
print(f"input={liste}")


def get_max_size(liste):
    max_x = 0
    max_y = 0
    for pair in liste:
        max_pair_x = pair[0]
        max_pair_y = pair[1]

        if max_pair_x > max_x:
            max_x = max_pair_x
        if max_pair_y > max_y:
            max_y = max_pair_y
    return max_x, max_y


def create_matrix(liste):
    max_x, max_y = get_max_size(liste)
    print(f"{max_x=} {max_y=}")
    # matrix = np.zeros((max_x + 1, max_y + 1))
    matrix = np.zeros((max_y + 1, max_x + 1))
    return matrix


#####################################
###### Before compression ###########
#####################################
matrix = create_matrix(liste)
for coor in liste:
    matrix[(coor[1], coor[0])] = 2

# plt.imshow(matrix)
# plt.show()


# %%
#########################
###### Compress #########
#########################


def get_mapping_rank_to_values(list_coordinates):
    uniques_sorted_coor = np.sort(list(set(list_coordinates)))
    dict_mapping = {}
    for i, x in enumerate(uniques_sorted_coor):
        dict_mapping[x] = i
    return dict_mapping


def compress_2d(liste):
    liste_x_val = []
    liste_y_val = []
    new_liste_vertices = []
    for vertice in liste:
        coor1, coor2 = vertice[0], vertice[1]
        liste_x_val.append(coor1)
        liste_y_val.append(coor2)

    dict_mapping_x = get_mapping_rank_to_values(liste_x_val)
    dict_mapping_y = get_mapping_rank_to_values(liste_y_val)

    new_liste_x = []
    new_liste_y = []
    new_liste_vertices = []
    for x, y in zip(liste_x_val, liste_y_val):
        rank_x = dict_mapping_x[x]
        rank_y = dict_mapping_y[y]
        new_liste_x.append(rank_x)
        new_liste_y.append(rank_y)
        new_liste_vertices.append((rank_x, rank_y))
    return new_liste_vertices


def add_vertice_to_matrix(list_vertices, matrix):
    for coor in list_vertices:
        matrix[(coor[1], coor[0])] = 2
    return matrix


new_liste_vertices = compress_2d(liste)
print(f"{new_liste_vertices}")
matrix = create_matrix(new_liste_vertices)
matrix = add_vertice_to_matrix(new_liste_vertices, matrix)

plt.imshow(matrix)
plt.show()

# %%


#################################
###### Fill the edges ###########
#################################
def get_next_vetice(i, liste_vertices):
    if i == len(liste_vertices) - 1:
        after_vertice = liste_vertices[0]
    else:
        after_vertice = liste_vertices[i + 1]
    return after_vertice[1], after_vertice[0]


def fill_edges(matrix, liste_vertices):
    for i, current_vertice in enumerate(liste_vertices):
        next_x, next_y = get_next_vetice(i, liste_vertices)
        current_x, current_y = current_vertice[1], current_vertice[0]
        print(f"current({current_x},{current_y}) ({next_x},{next_y})")
        delta_x = abs(next_x - current_vertice[1])
        delta_y = abs(next_y - current_vertice[0])
        print(f"{delta_x=} {delta_y=}")
        if delta_x == 0:
            miny = min(next_y, current_y)
            matrix[current_x, miny : miny + delta_y + 1] = 1
        elif delta_y == 0:
            minx = min(next_x, current_x)
            matrix[minx : minx + delta_x + 1, current_y] = 1
        else:
            raise Exception("not a 0 in delta")
        print("*" * 20)
    return matrix


matrix = create_matrix(new_liste_vertices)
matrix = add_vertice_to_matrix(new_liste_vertices, matrix)
matrix = fill_edges(matrix, new_liste_vertices)
print(matrix)
plt.imshow(matrix)
plt.show()
# %%
import sys

sys.setrecursionlimit(50_000)

matrix = create_matrix(new_liste_vertices)
matrix = add_vertice_to_matrix(new_liste_vertices, matrix)
matrix = fill_edges(matrix, new_liste_vertices)

#################################
###### Implement DFS ###########
#################################
input_x = 100
input_y = 100


def dfs(matrix, input_x, input_y):
    list_neigbors = product(
        [input_x + dx for dx in [-1, 0, 1]], [input_y + dy for dy in [-1, 0, 1]]
    )
    for x, y in list_neigbors:
        if (x, y) != (input_x, input_y):
            if matrix[x, y] == 0:
                matrix[x, y] = 1
                dfs(matrix, x, y)
    return matrix


matrix = dfs(matrix, input_x, input_y)
plt.imshow(matrix)
plt.show()


# %%
###################################
###### Compute the area ###########
###################################
def compute_area(pair_value):
    coor1, coor2 = pair_value[0], pair_value[1]
    largeur = abs(coor1[0] - coor2[0]) + 1
    longueur = abs(coor1[1] - coor2[1]) + 1
    area = largeur * longueur
    return area


def is_sub_matrix_valid(matrix, x1, y1, x2, y2):
    minx = min(x1, x2)
    miny = min(y1, y2)
    maxx = max(x1, x2)
    maxy = max(y1, y2)

    if minx == maxx:
        is_null: bool = matrix_is_null(matrix[minx, miny:maxy])
    elif miny == maxy:
        is_null: bool = matrix_is_null(matrix[minx:maxx, miny])
    else:
        is_null: bool = matrix_is_null(matrix[minx:maxx, miny:maxy])
    if is_null:
        return False
    else:
        return True


def matrix_is_null(matrix):
    result = np.where(matrix == 0)[0]
    if result.shape[0] > 0:
        return False
    return True


list_combinations = combinations(new_liste_vertices, 2)
liste_area = []
liste_distance = []
list_pair_values = []
for pair_value in list_combinations:
    coor1, coor2 = pair_value[0], pair_value[1]
    x1, y1 = coor1[0], coor1[1]
    x2, y2 = coor2[0], coor2[1]
    if is_sub_matrix_valid(matrix, x1, y1, x2, y2):
        list_pair_values.append(pair_value)
        area = compute_area(pair_value)
        print(f"{pair_value=}: Area={area}")
        liste_area.append(area)
    else:
        print("Not valid")
print(f"Answer={np.max(liste_area)}")

# %%
# too low 18360
