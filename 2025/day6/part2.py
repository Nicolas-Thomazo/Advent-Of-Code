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


def replace_in_string(string):
    new_string = ""
    for char in string:
        if char == " ":
            new_string += "0"
        else:
            new_string += char
    return new_string


def count(input, row):
    list_count_numbers = input[row].split(" ")
    list_count = []
    for x in list_count_numbers:
        if x != "":
            list_count.append(x)
    return len(list_count)


def build_arrays(input):
    operations = input[-1].split(" ")
    operations_list = []
    for op in operations:
        if op != "":
            operations_list.append(op)
    return np.array(operations_list)


USE_DEMO = False
input = get_content(use_demo=USE_DEMO)
operations = build_arrays(input)

full_list = []
list_correct_numbers = []
for i in range(len(input[0])):
    x1 = input[0][i]
    x2 = input[1][i]
    x3 = input[2][i]
    x4 = input[3][i]
    if USE_DEMO:
        x4 = " "

    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    list_condition = [True if x in numbers else False for x in [x1, x2, x3, x4]]
    if any(list_condition):
        list_correct_numbers.append(f"{x1}{x2}{x3}{x4}")
    else:
        print(f"Next number {list_correct_numbers}")
        full_list.append(list_correct_numbers)
        list_correct_numbers = []
full_list.append(list_correct_numbers)
print(f"{full_list=}")
# %%
all_sum = 0
for liste, operation in zip(full_list, operations):
    row_calcul = 0
    for elem in liste:
        if operation == "+":
            row_calcul += int(elem)
        else:
            if row_calcul == 0:
                row_calcul = int(elem)
            else:
                row_calcul *= int(elem)
    print(f"{liste=} : {row_calcul=}")
    all_sum += row_calcul
print(f"{all_sum=}")
# %%
