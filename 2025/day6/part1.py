# %%
# %%
from pathlib import Path

import numpy as np

######################
#### Initialise ######
######################


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


input = get_content(use_demo=False)


def build_arrays(input):
    operations = input[-1].split(" ")
    operations_list = []
    for op in operations:
        if op != "":
            operations_list.append(op)
    list_numbers = []
    for sub_list_numbers in input[:-1]:
        split_sub_list = sub_list_numbers.split(" ")
        print(f"{split_sub_list=}")
        temp_sub_list_int = []
        for string in split_sub_list:
            if string != "":
                temp_sub_list_int.append(int(string))
        list_numbers.extend(temp_sub_list_int)
    return np.array(operations_list), np.array(list_numbers)


operations, array_numbers = build_arrays(input)
print(f"{array_numbers=}")

different_operations = set(operations)
print(f"{different_operations=}")
size = len(operations)
array_numbers = array_numbers.reshape(-1, size)
print(f"\narray_numbers=\n{array_numbers}")
# %%
index = np.where(operations == "+")[0]
array_op = array_numbers[:, index]
sum_array = array_op.sum(axis=0)

index = np.where(operations == "*")[0]
array_op = array_numbers[:, index]
mult_array = np.prod(array_op, axis=0)
result = np.sum(sum_array) + np.sum(mult_array)
print(f"PART 1:{result=}")
# %%
