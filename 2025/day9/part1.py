# %%
from itertools import combinations
from pathlib import Path

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


# %%
def compute_area(pair_value):
    coor1, coor2 = pair_value[0], pair_value[1]
    largeur = abs(coor1[0] - coor2[0]) + 1
    longueur = abs(coor1[1] - coor2[1]) + 1
    area = largeur * longueur
    return area


list_combinations = combinations(liste, 2)
liste_area = []
liste_distance = []
list_pair_values = []
for pair_value in list_combinations:
    coor1, coor2 = pair_value[0], pair_value[1]
    list_pair_values.append(pair_value)
    area = compute_area(pair_value)
    print(f"{pair_value=}: Area={area}")
    liste_area.append(area)

print(f"Answer={np.max(liste_area)}")
