# %%
from itertools import combinations, product
from pathlib import Path

import numpy as np

######################
#### Initialise ######
######################
USE_DEMO = False
LARGEST_CIRCUIT = 3
SHORTEST_PAIRS = 10
if not USE_DEMO:
    SHORTEST_PAIRS = 1000


def get_content(use_demo: bool) -> list:
    print("*" * 50, "Import Data", "*" * 50)
    if use_demo:
        file = Path("input_example.txt")
    else:
        file = Path("input.txt")

    with open(file) as f:
        content: str = f.read()
    content_list: list[str] = content.split("\n")
    if content_list[-1] == "":
        content_list = content_list[:-1]
    return content_list


input = get_content(use_demo=USE_DEMO)
# input = ["162,817,812", "57,618,57", "906,360,560"]
input_int = []
for x in input:
    list_str = x.split(",")
    list_int = [int(x) for x in list_str]
    input_int.append(tuple(list_int))
print(f"{input_int}")
# %%
list_all_combinations = []
for x in combinations(input_int, 2):
    # print("-", x)
    list_all_combinations.append(x)
print(f"size={len(list_all_combinations)}")


# %%
def compute_distance(junction_box_1, junction_box_2):
    diff = np.array(junction_box_1) - np.array(junction_box_2)
    return np.sqrt(np.sum(diff**2))


junction_box_1 = (162, 817, 812)
junction_box_2 = (57, 618, 57)

a = compute_distance(junction_box_1, junction_box_2)

list_distances = []
for x in list_all_combinations:
    dist = compute_distance(x[0], x[1])
    list_distances.append(dist)
print(f"{list_distances=}")

list_index = np.argsort(list_distances)


# %%
def delete_in_place(lst, indices_to_delete):
    for i in sorted(indices_to_delete, reverse=True):
        del lst[i]
a=[0,1,2,3,4,5]
delete_in_place(a,[2,3])
print(a)
#%%

def merge_circuit(list_circuits: list, box1, box2,set_visited):
    # On va regarder si box1 ou box2 est dans un circuit
    #print(f"Size of circuits={len(list_circuits)}")
    circuit_to_merge = []
    for circuit_index, circuit in enumerate(list_circuits):
        if box1 in circuit or box2 in circuit:
            # Si c'est le cas on l'ajoute aux circuits a merge
            circuit_to_merge.append(circuit_index)
    # Si on doit merge des circuits, on pop les index des circuits et on ajoute le nouveau
    if circuit_to_merge:
        print(f"Merge {len(circuit_to_merge)} circuits {box1} {box2}")
        for x in circuit_to_merge:
            print(list_circuits[x])
        new_circuit = set()
        for pop_idx in circuit_to_merge:
            pop_circuit = list_circuits[pop_idx]
            # print(f"{pop_circuit=}")
            new_circuit = new_circuit.union(pop_circuit)
        new_circuit = new_circuit.union({box1, box2})
        set_visited=set_visited.union({box1,box2})
        #print(f"{new_circuit=}")
        delete_in_place(list_circuits, circuit_to_merge)
        list_circuits.append(new_circuit)
        #print(f"New size is {len(list_circuits)}")
    return list_circuits,set_visited


list_circuits_test = [set({"A", "C"}), set("B")]
box1 = "A"
box2 = "B"
list_circuits,visited=merge_circuit(list_circuits_test, box1, box2,set())
print(f"{list_circuits=}. {visited=}")
# %%
list_circuits = []
set_visited = set()
for i, index in enumerate(list_index[:SHORTEST_PAIRS]):
    #print("*" * 15, f"{i=}", "*" * 15)
    box1, box2 = list_all_combinations[index]
    # Si box 1 et 2 n'ont jamais été vu elles forment un nouveau circuit
    if box1 not in set_visited and box2 not in set_visited:
        list_circuits.append(set((box1, box2)))
        set_visited.add(box1)
        set_visited.add(box2)
        #print(f"Never seend add box 1:{box1} and box 2:{box2} as new circuit ")
    else:
        list_circuits,set_visited = merge_circuit(list_circuits, box1, box2,set_visited)

    # print(f"Current circuits ={list_circuits}")
# print(f"{set_visited=}")
print(f"Contains {len(list_circuits)} circuits")
size_circuits = []
for x in list_circuits:
    size_circuits.append(len(x))
print(size_circuits)
# %%
sorted_size = np.sort(size_circuits)[::-1][:LARGEST_CIRCUIT]
result=1
print(f"Sorted size = {sorted_size}")
for x in sorted_size:
    result*=x
print(f"Result={result}")
# %%
