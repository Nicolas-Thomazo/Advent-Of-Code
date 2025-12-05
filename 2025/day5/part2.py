# %%
from collections import deque
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
    liste_ingredients = content.split("\n\n")

    fresh_ingredients = liste_ingredients[0].split("\n")
    list_fresh_ingredients = []
    for fresh in fresh_ingredients:
        range_values = fresh.split("-")
        first, last = int(range_values[0]), int(range_values[1])
        list_fresh_ingredients.append((first, last))
    return list_fresh_ingredients


fresh_ingredients = get_content(use_demo=False)
print(f"{fresh_ingredients=}")


# %%
def get_queue_sorted(fresh_ingredients):
    array_min = []
    for elem in fresh_ingredients:
        array_min.append(elem[0])

    sorted_index = np.argsort(array_min)

    queue_sorted = deque()
    for i in range(len(fresh_ingredients)):
        queue_sorted.append(fresh_ingredients[sorted_index[i]])
    print(f"{queue_sorted=}")
    return queue_sorted


def merge_if_needed(low_elem, upper_elem):
    new_elem = None
    if low_elem is None or upper_elem is None:
        return new_elem
    if upper_elem[0] <= low_elem[1]:
        new_elem = (low_elem[0], max(low_elem[1], upper_elem[1]))
    return new_elem


queue_sorted = get_queue_sorted(fresh_ingredients)

# %%
queue_sorted = get_queue_sorted(fresh_ingredients)
not_overllapping_queue = []

while len(queue_sorted) != 0:
    if len(not_overllapping_queue) == 0:
        last_not_overlapping = None
    else:
        last_not_overlapping = not_overllapping_queue[-1]

    first_in_queue = queue_sorted.popleft()
    new = merge_if_needed(last_not_overlapping, first_in_queue)
    if new is None:
        not_overllapping_queue.append(first_in_queue)
    else:
        not_overllapping_queue.pop()
        not_overllapping_queue.append(new)

    print(f"--{not_overllapping_queue=}")

# %%
count = 0
for elem in not_overllapping_queue:
    count += elem[1] - elem[0] + 1

print(f"{count=}")

# %%
