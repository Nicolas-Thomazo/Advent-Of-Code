# %%
from itertools import combinations
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
    matrix = np.zeros((max_x+1, max_y+1))
    return matrix

matrix = create_matrix(liste)


# %%
def compute_area(pair_value):
    coor1, coor2 = pair_value[0], pair_value[1]
    largeur = abs(coor1[0] - coor2[0]) + 1
    longueur = abs(coor1[1] - coor2[1]) + 1
    area = largeur * longueur
    return area


def fill_matrix(matrix, coor1, coor2):
    matrix[coor1]=2
    matrix[coor2]=2
    delta_x=abs(coor1[0]-coor2[0])
    delta_y=abs(coor1[1]-coor1[1])
    min_x=min(coor1[0],coor2[0])
    min_y=min(coor1[1],coor1[1])
    print(f"{delta_x=} {delta_y=} {min_x=} {min_y=}")

    if delta_y==0:
        index_null=matrix[min_x:min_x+delta_x,min_y]==0
        matrix[min_x:min_x+delta_x,min_y][index_null]=1
    elif delta_x==0:
        index_null=matrix[min_x,min_y:min_y+delta_y]==0
        matrix[min_x,min_y:min_y+delta_y][index_null]=1
    else:
        raise Exception("Error")
    # matrix[min_x]
    return matrix

list_combinations = combinations(liste, 2)
matrix = create_matrix(liste)
print(f"{matrix=}")

liste_area = []
list_pair_values = []
for pair_value in list_combinations:
    print("a")
    coor1, coor2 = pair_value[0], pair_value[1]
    list_pair_values.append(pair_value)
    matrix=fill_matrix(matrix=matrix, coor1=coor1, coor2=coor2)
    # area = compute_area(pair_value)
    # print(f"{pair_value=}: Area={area}")
    # liste_area.append(area)

# print(f"Answer={np.max(liste_area)}")
# print(f"{matrix=}")
plt.imshow(matrix)
plt.show()
# %%
