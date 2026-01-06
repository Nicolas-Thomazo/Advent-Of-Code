# %%
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


liste = get_content(use_demo=True)
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

plt.imshow(matrix)
plt.show()


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


matrix = create_matrix(new_liste_vertices)
matrix = add_vertice_to_matrix(new_liste_vertices, matrix)

for i, current_vertice in enumerate(new_liste_vertices):
    next_x, next_y = get_next_vetice(i, new_liste_vertices)
    current_x, current_y = current_vertice[1], current_vertice[0]
    print(f"{current_vertice=} {next_x},{next_y}")
    delta_x = next_x - current_vertice[1]
    delta_y = next_y - current_vertice[0]
    print(f"{delta_x=} {delta_y=}")
    if delta_x == 0:
        matrix[current_x, current_y : current_y + delta_y] = 1
    if delta_y == 0:
        matrix[current_x : current_x + delta_x, current_y] = 1

plt.imshow(matrix)
plt.show()
# %%
