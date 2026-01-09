# %%
import sys
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

use_demo=False
liste = get_content(use_demo=use_demo)
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
    matrix = np.zeros((max_x + 1, max_y + 1))
    return matrix


#####################################
###### Before compression ###########
#####################################
matrix = create_matrix(liste)
for coor in liste:
    matrix[(coor[0], coor[1])] = 2

if use_demo:
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
    return new_liste_vertices, dict_mapping_x, dict_mapping_y


def add_vertice_to_matrix(list_vertices, matrix):
    for coor in list_vertices:
        matrix[
            (
                coor[0],
                coor[1],
            )
        ] = 2
    return matrix


new_liste_vertices, dict_mapping_x, dict_mapping_y = compress_2d(liste)
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
    return after_vertice[0], after_vertice[1]


def fill_edges(matrix, liste_vertices):
    for i, current_vertice in enumerate(liste_vertices):
        next_x, next_y = get_next_vetice(i, liste_vertices)
        current_x, current_y = current_vertice[0], current_vertice[1]
        print(f"current({current_x},{current_y}) ({next_x},{next_y})")
        delta_x = abs(next_x - current_vertice[0])
        delta_y = abs(next_y - current_vertice[1])
        print(f"{delta_x=} {delta_y=}")
        if delta_x == 0:
            miny = min(next_y, current_y)
            matrix[current_x, miny : miny + delta_y + 1] = 1
        elif delta_y == 0:
            minx = min(next_x, current_x)
            matrix[minx : minx + delta_x + 1, current_y] = 1
        else:
            raise ValueError("not a 0 in delta")
        print("*" * 20)
    return matrix


matrix = create_matrix(new_liste_vertices)
matrix = add_vertice_to_matrix(new_liste_vertices, matrix)
matrix = fill_edges(matrix, new_liste_vertices)
print(matrix)
plt.imshow(matrix)
plt.show()
# %%

sys.setrecursionlimit(50_000)

matrix = create_matrix(new_liste_vertices)
matrix = add_vertice_to_matrix(new_liste_vertices, matrix)
matrix = fill_edges(matrix, new_liste_vertices)

#################################
###### Implement DFS ###########
#################################
input_x = 100
input_y = 100
if use_demo:
    input_x=2
    input_y=1

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
    largeur = abs(coor1[0] - coor2[0])
    longueur = abs(coor1[1] - coor2[1])
    area = largeur * longueur
    return area


def is_sub_matrix_valid(matrix, x1, y1, x2, y2):
    minx = min(x1, x2)
    miny = min(y1, y2)
    maxx = max(x1, x2)
    maxy = max(y1, y2)
    is_polygon_valid = True
    slice_x = slice(minx, maxx)
    if minx == maxx:
        slice_x = minx

    slice_y = slice(miny, maxy)
    if miny == maxy:
        slice_y = slice(miny)

    is_null: bool = matrix_is_null(matrix[slice_x, slice_y])
    if is_null:
        is_polygon_valid = False
    return is_polygon_valid, slice_x, slice_y


def matrix_is_null(matrix):
    result = np.where(matrix == 0)[0]
    if result.shape[0] > 0:
        return True
    return False


def plot_rectangle(matrix, slice_xy, save=False, number=0, show=True):
    img_name = Path(f"images/ploygon_{number}.png")
    if not show and img_name.exists():
        print("skip")
        return None
    copy_matrix = matrix.copy()
    copy_matrix[slice_xy[0], slice_xy[1]] = 2
    plt.imshow(copy_matrix)
    if save:
        plt.savefig(img_name)
    if show:
        plt.show()
    plt.close()
    return None


list_combinations = list(combinations(new_liste_vertices, 2))
liste_area = []
list_slice = []
list_valid_pairs = []
count = 0
valid_count = 0
for pair_value in list_combinations:
    coor1, coor2 = pair_value[0], pair_value[1]
    x1, y1 = coor1[0], coor1[1]
    x2, y2 = coor2[0], coor2[1]
    is_valid, slice_x, slice_y = is_sub_matrix_valid(matrix, x1, y1, x2, y2)

    if is_valid:
        area = compute_area(pair_value)
        liste_area.append(area)
        list_slice.append((slice_x, slice_y))
        list_valid_pairs.append(pair_value)

        # print(f"Valid {pair_value=}: Area={area}")
        # plot_rectangle(
        #     matrix, (slice_x, slice_y), save=True, number=valid_count, show=False
        # )
        valid_count += 1
    count += 1

    #
    # if count % 5 == 0:
    #     copy_matrix = matrix.copy()
    #     copy_matrix[slice_x, slice_y] = 0.5
    #     plt.imshow(copy_matrix)
    #     plt.show()
print(f"Valids areas = {len(liste_area)}")
# %%


def get_uncompressed(pair_1, pair_2):
    mapping_x_keys = list(dict_mapping_x.keys())
    mapping_y_keys = list(dict_mapping_y.keys())

    pair1_x_uncompressed = mapping_x_keys[pair_1[0]]
    pair2_x_uncompressed = mapping_x_keys[pair_2[0]]

    pair1_y_uncompressed = mapping_y_keys[pair_1[1]]
    pair2_y_uncompressed = mapping_y_keys[pair_2[1]]

    pair1_uncompressed = pair1_x_uncompressed, pair1_y_uncompressed
    pair2_uncompressed = pair2_x_uncompressed, pair2_y_uncompressed

    pair_uncompressed = (
        pair1_uncompressed,
        pair2_uncompressed,
    )
    return pair_uncompressed


uncompressed_areas = []
for i, pair_area in enumerate(liste_area):
    pair_1, pair_2 = list_valid_pairs[i]
    pair_uncompressed = get_uncompressed(pair_1, pair_2)
    area = compute_area(pair_uncompressed)
    uncompressed_areas.append(area)

index = np.argmax(uncompressed_areas)
print(f"Answer:{uncompressed_areas[index]=} ")


def plot_rectangle_v2(matrix, slice_xy, pair_1, pair2):
    copy_matrix = matrix.copy()
    copy_matrix[slice_xy[0], slice_xy[1]] = 2
    print(f"matrix is fill here {np.where(copy_matrix == 2)[0].shape}")
    copy_matrix[pair_1] = 3
    copy_matrix[pair2] = 3
    plt.imshow(copy_matrix)
    plt.show()
    return copy_matrix


# copy_matrix = plot_rectangle_v2(matrix, slices_max, pair_1, pair_2)


# 459405162
# 570606225 to low
# 1772419530 to high
# 1733493120 no
# 1733385357 no
# 1613305596 --> righ answer
# index_sorted = np.argsort(uncompressed_areas)
# pair_area[index_sorted][:]
print(f"{np.sort(uncompressed_areas)}")
# %%
pair = list_valid_pairs[1080]
slicee=list_slice[1080]
print(f"{pair=}")
plot_rectangle_v2(matrix, slicee,pair[0], pair[1])
#%%
pair = list_valid_pairs[1076]
slicee=list_slice[1076]
print(f"{pair=}")

plot_rectangle_v2(matrix, slicee,pair[0], pair[1])

# %%
def find_max_area(liste_area, list_slice, index):
    list_index_sorted = np.argsort(liste_area)[::-1]
    sorted_areas = np.sort(liste_area)[::-1]
    list_slice_sorted = np.array(list_slice)[list_index_sorted]
    max_area = sorted_areas[index]
    slices_max = list_slice_sorted[index]
    print(f"Answer:{max_area=} {slices_max=}")
    return slices_max


for i in range(3):
    print(f"Last max value is: {i}")
    slice_xy = find_max_area(liste_area, list_slice, i)
    plot_rectangle(matrix, slice_xy, save=True, number=i)
# %%
