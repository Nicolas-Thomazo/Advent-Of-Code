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


list_signal: list[str] = get_content(use_demo=False)
array_signal: NDArray = get_numpy_array(list_signal)
matrix_input = array_signal.copy()

#####################
#### Resolution #####
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


def mark_antinodes_on_matrix(matrix_copy, antinode_1, antinode_2):
    if antinode_1[0] < matrix_copy.shape[0] and antinode_1[1] < matrix_copy.shape[1]:
        matrix_copy[antinode_1] = "#"  # type: ignore
    if antinode_2[0] < matrix_copy.shape[0] and antinode_2[1] < matrix_copy.shape[1]:
        matrix_copy[antinode_2] = "#"  # type: ignore
    return matrix_copy


def add_antinode_to_set(set_antinodes, antinode, shape_matrix):
    if (
        antinode[0] < shape_matrix[0]
        and antinode[0] >= 0
        and antinode[1] < shape_matrix[1]
        and antinode[1] >= 0
    ):
        set_antinodes.add(antinode)
    return set_antinodes


list_nodes_values: list[str] = get_all_nodes_values(matrix_input)
print("*" * 50, "Get nodes coordinates", "*" * 50)
print(
    f"Input matrix contains {len(list_nodes_values)} différentes values: {','.join(list_nodes_values)}"
)
DEBUG_MODE = False
set_antinodes = set()
matrix_copy = matrix_input.copy()
for node_value in list_nodes_values:
    (coor_Xa, coor_Ya) = np.where(matrix_input == node_value)
    list_vertices = list(zip(coor_Xa, coor_Ya))
    combinations_vertices = list(combinations(list_vertices, r=2))
    if DEBUG_MODE:
        print(
            "-" * 10,
            f"Node value: {node_value}, contains {len(list_vertices)} vertices, {len(combinations_vertices)} pairs combinations",
            "-" * 10,
        )
    for node_1, node_2 in combinations_vertices:
        antinode_1, antinode_2 = compute_coordinates_antinodes(node_1, node_2)
        add_antinode_to_set(set_antinodes, antinode_1, matrix_input.shape)
        add_antinode_to_set(set_antinodes, antinode_2, matrix_input.shape)
        if DEBUG_MODE:
            print(f"{node_1=} {node_2=}")
            mark_antinodes_on_matrix(matrix_copy, antinode_1, antinode_2)
            print(matrix_copy)

print("*" * 25, f"Total antinodes found: {len(set_antinodes)}", "*" * 25)

# %%
