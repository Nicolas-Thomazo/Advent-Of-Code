# %%
from itertools import combinations
from pathlib import Path

import numpy as np
from numpy._typing._array_like import NDArray

######################
#### Initialise ######
######################


def get_content(use_demo: bool) -> list[str]:
    print("*" * 50, "Import Data", "*" * 50)
    if use_demo:
        file = Path("input_example.txt")
    else:
        file = Path("input.txt")

    with open(file) as f:
        content: str = f.read()
    content_list: list[str] = content.split("\n")
    clean_list = []
    for x in content_list:
        if x != "":
            clean_list.append(x)
    if len(clean_list) != len(content_list):
        print(
            f"Deletion and cleaning, len final list={len(clean_list)} (vs {len(content_list)})"
        )
    return clean_list


def get_numpy_array(list_signal) -> NDArray:
    all_arrays: list = []
    for one_line in list_signal:
        all_arrays.append(np.array(list(one_line)))
    array_signal: NDArray = np.array(all_arrays)
    return array_signal


list_signal: list[str] = get_content(use_demo=True)
array_signal: NDArray = get_numpy_array(list_signal)
matrix_input = array_signal.copy()

# %%

######################
#### Methodo 1 #######
######################
# Step 1: Récupérer la liste des sommets avec leur coordonnées
# {"a": [(0,0),(1,0)],"b"...}

# Step 2: Pour chaque catégorie de sommets on calcul les coordonnées des antinodes
# y=ax+b => on calcul a et b
# b=y0-ax0 et b=y1-ax1 ==> a=(y1-y0)/(x1-x0) b=y1-ax1
# distance euclidienne=racine((y1-y0)^2+(x1-x0)2)
# distance euclidienne de antinode et (x0,y0) = 2* distance antinode et (y1,x1)


def eucledian_distance(x0, y0, x1, y1):
    distance_x = x1 - x0  # np.square(x1 - x0)
    distance_y = y1 - y0  # np.square(y1 - y0)
    return distance_y + distance_x  # np.sqrt(distance_y + distance_x)


def compare_distances(x_antinode, y_antinode, coor_x_node, coor_y_node):
    x0 = coor_x_node[0]
    x1 = coor_x_node[1]
    y0 = coor_y_node[0]
    y1 = coor_y_node[1]
    distance_node_1 = eucledian_distance(x_antinode, y_antinode, x0, y0)
    distance_node_2 = eucledian_distance(x_antinode, y_antinode, x1, y1)
    return distance_node_1, distance_node_2


def compute_y_value(x, a, b):
    result = np.float64(a * x + b)
    # assert result.is_integer(), f"result is {result}, it should be an integer"
    return result


def check_right_distance(d1, d2):
    if 2 * d1 == d2 or 2 * d2 == d1:
        return True
    return False


# def find_all_aligned_values(list_coor_x_node, list_coor_y_node):
#     a, b = compute_coeficient(list_coor_x_node, list_coor_y_node)
#     raw_liste_x = np.arange(0, array_signal.shape[0])
#     liste_x = []
#     liste_y = []
#     for x_antinode in raw_liste_x:
#         y_antinode = np.float64(a * x_antinode + b)
#         if y_antinode.is_integer():
#             liste_x.append(x_antinode)
#             liste_y.append(int(y_antinode))
#     return liste_x, liste_y
def find_all_aligned_values(node_1: tuple[int, int], node_2: tuple[int, int]):
    a, b = compute_coeficient(node_1, node_2)
    raw_liste_x = np.arange(0, array_signal.shape[0])
    liste_x = []
    liste_y = []
    for x_antinode in raw_liste_x:
        y_antinode = np.float64(a * x_antinode + b)
        if y_antinode.is_integer():
            liste_x.append(x_antinode)
            liste_y.append(int(y_antinode))
    return liste_x, liste_y


def find_antinodes_vertices(node_1: tuple, node_2: tuple):
    # coor_x_arr = [node_1[0], node_2[0]]
    # corr_y_arr = [node_1[1], node_2[1]]
    vertices_antinodes = []
    liste_x, liste_y = find_all_aligned_values(node_1, node_2)
    for x_antinode, y_antinode in zip(liste_x, liste_y):
        d1, d2 = compare_distances(x_antinode, y_antinode, coor_Xa, coor_Ya)
        condition_respected = check_right_distance(d1, d2)
        if condition_respected:
            vertices_antinodes.append((x_antinode, y_antinode))
    return vertices_antinodes


# %%
#####################
#### Breshenman #####
#####################


def compute_coeficient(node_1: tuple[int, int], node_2: tuple[int, int]):
    x0, y0 = node_1
    x1, y1 = node_2
    if x1 == x0:
        a = float("inf")
        b = float("inf")
        return a, b
    a = (y1 - y0) / (x1 - x0)
    b = y1 - a * x1
    return a, b


def compute_equation(node_1: tuple[int, int], node_2: tuple[int, int], t: float):
    x = node_1[0] + t * (node_2[0] - node_1[0])
    y = node_1[1] + t * (node_2[1] - node_1[1])
    return x, y


def compute_coordinates_antinodes(
    node_1: tuple[int, int], node_2: tuple[int, int]
) -> tuple[tuple[float, float], tuple[float, float]]:
    x, y = compute_equation(node_1, node_2, 2)
    antinode_1 = (x, y)
    x2, y2 = compute_equation(node_1, node_2, -1)
    antinode_2 = (x2, y2)
    return antinode_1, antinode_2


def get_all_nodes_values(matrix_input):
    unique_value_matrix = set(matrix_input.flatten())
    unique_value_matrix.remove(".")
    return list(unique_value_matrix)


list_nodes_values: list[str] = get_all_nodes_values(matrix_input)
print("*" * 50, "Get nodes coordinates", "*" * 50)
print(
    f"Input matrix contains {len(list_nodes_values)} différentes values: {','.join(list_nodes_values)}"
)
DEBUG_MODE = True
for node_value in list_nodes_values[:1]:
    (coor_Xa, coor_Ya) = np.where(matrix_input == node_value)
    list_vertices = list(zip(coor_Xa, coor_Ya))
    combinations_vertices = list(combinations(list_vertices, r=2))
    if DEBUG_MODE:
        print(
            "-" * 10,
            f"Node value: {node_value}, contains {len(list_vertices)} vertices, {len(combinations_vertices)} pairs combinations",
            "-" * 10,
        )
    for node_1, node_2 in combinations_vertices[:3]:
        matrix_copy = matrix_input.copy()
        matrix_copy[node_1] = "X"
        matrix_copy[node_2] = "Y"
        print(f"{node_1=} {node_2=}")
        # print(matrix_copy)
        a, b = compute_coeficient(node_1, node_2)
        # if a == np.inf:
        #     print("Vertical line, skipping")
        # else:
        antinode_1, antinode_2 = compute_coordinates_antinodes(node_1, node_2)
        if (
            antinode_1[0] < matrix_copy.shape[0]
            and antinode_1[1] < matrix_copy.shape[1]
        ):
            matrix_copy[antinode_1] = "A"
        if (
            antinode_2[0] < matrix_copy.shape[0]
            and antinode_2[1] < matrix_copy.shape[1]
        ):
            matrix_copy[antinode_2] = "A"
        print(matrix_copy)
        # vertices_antinodes = find_antinodes_vertices(node_1, node_2)
        # print(f"{vertices_antinodes=}")

# %%
liste_x, liste_y = find_all_aligned_values(coor_Xa, coor_Ya)
matrix_copy = matrix_input.copy()
matrix_copy[liste_x, liste_y] = "P"
print(f"Possibilities is\n{matrix_copy}")

for x_antinode, y_antinode in zip(liste_x, liste_y):
    d1, d2 = compare_distances(x_antinode, y_antinode, coor_Xa, coor_Ya)
    condition = check_right_distance(d1, d2)
    if condition:
        print(f"condition respected for {x_antinode=},{y_antinode=}")
        matrix_input[x_antinode, y_antinode] = "#"
print(matrix_input)
# %%
