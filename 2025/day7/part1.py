# %%
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
    matrix = None
    for liste in content_list:
        if matrix is None:
            matrix = np.array(list(liste))
        else:
            matrix = np.vstack((matrix, np.array(list(liste))))
    return matrix


matrix = get_content(use_demo=False)
print(matrix)

start = np.where(matrix == "S")
start = start[0][0], start[1][0]
# print(f"{start=}")


def is_bottom(matrix, x):
    shape = matrix.shape
    if x >= shape[0]:
        return True
    else:
        return False


def y_is_valid(matrix, y):
    shape = matrix.shape
    if y < shape[1]:
        return True
    else:
        return False


def can_go_down(matrix, x, y):
    down_x = x + 1
    if not is_bottom(matrix, down_x):
        down_value = matrix[down_x, y]
        if down_value == ".":
            return True
        elif down_value == "^":
            return False
        # else:
        #     raise ValueError("Don't except anything else")
    else:
        print(f"reach bottom for {down_x, y}")
        return False


def add_to_queue(matrix, queue, down, old_x, old_y, count_split):
    if down:
        new_position = old_x + 1, old_y
        print(f"Go down {new_position}")
        matrix[new_position] = "|"  # type: ignore
        queue.append(new_position)
    else:
        count_split += 1
        left_value = (old_x, old_y - 1)
        right_value = (old_x, old_y + 1)
        if not is_bottom(matrix, left_value[0]) and y_is_valid(matrix, left_value[1]):
            queue.append(left_value)
        if not is_bottom(matrix, right_value[0]) and y_is_valid(matrix, right_value[1]):
            queue.append(right_value)
    return matrix, queue, count_split


y_is_valid(matrix, 15)
# %%
matrix = get_content(use_demo=False)
queue = [start]
is_arrived = False
visited = set()
i = 0
count_split = 0

while len(queue) != 0:  # (not is_arrived) or
    print(f"{queue=}")
    print(matrix)
    old_coordinates = queue.pop()
    old_x = old_coordinates[0]
    old_y = old_coordinates[1]

    if (old_x, old_y) not in visited:
        visited.add((old_x, old_y))
        down = can_go_down(matrix, old_x, old_y)
        reach_bottom = is_bottom(matrix, old_x + 1)
        i += 1
        if not reach_bottom:
            matrix, queue, count_split = add_to_queue(
                matrix, queue, down, old_x, old_y, count_split
            )
print(matrix)
print(f"Result part 1={count_split}")
# %%
