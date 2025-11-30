# %%
from collections import deque
from pathlib import Path

# from queue import Queue
######################
#### Initialise ######
######################


def get_content(use_demo: bool) -> str:
    print("*" * 50, "Import Data", "*" * 50)
    if use_demo:
        file = Path("input_example.txt")
    else:
        file = Path("input.txt")

    with open(file) as f:
        content: str = f.read()
    content_list: list[str] = content.split("\n")
    return "".join(content_list)


input = get_content(use_demo=False)
print(f"{input=}")


def decompose_queue(input: str):
    decomposed = deque()
    decomposed_index = deque()
    list_decomposed = []
    index_file = 0
    for index_input in range(len(input)):
        char = input[index_input]
        value = int(char)
        if index_input % 2 == 0:
            temp_list = []
            temp_list_index = []
            for _ in range(value):
                temp_list.append(index_file)
                temp_list_index.append(len(list_decomposed))
                list_decomposed.append(index_file)
            decomposed.append(temp_list)
            decomposed_index.append(temp_list_index)
            index_file += 1
        else:
            liste_dot = ["."] * value
            list_decomposed.extend(liste_dot)
    return decomposed, decomposed_index, list_decomposed


deque_decomposed, deque_decomposed_index, list_decomposed = decompose_queue(input)
print(f"{deque_decomposed=}")
print(f"{deque_decomposed_index=}")
print(f"{list_decomposed=}")


# %%
def parcours_list_decomposed(list_decomposed, value_queue):
    index_result = None
    is_valid = False
    for j in range((len(list_decomposed))):
        if list_decomposed[j] == ".":
            if len(value_queue) == 1:
                is_valid = True
                index_result = j
                break
            for increment in range(1, len(value_queue)):
                # print(f"Checking index{j} {increment}:", j + increment,"len list_decomposed:", len(list_decomposed))
                if j + increment < len(list_decomposed) and list_decomposed[j + increment] == ".":
                    is_valid = True
                else:
                    is_valid = False
                    break
            if is_valid:
                index_result = j
                break
    # if is_valid:
    #     print(f"Valid element found at index {index_result}")
    # else:
    #     print("No valid element found")
    return is_valid, index_result

# %%
elem_in_queue = len(deque_decomposed)

for i in range(elem_in_queue):
    value = deque_decomposed.pop()
    index_value = deque_decomposed_index.pop()
    is_valid, index_result = parcours_list_decomposed(list_decomposed, value)
    if is_valid and index_result < index_value[0]:
        for k in range(len(value)):
            list_decomposed[index_result + k] = value[k]
        for idx in index_value:
            list_decomposed[idx] = "."

print(list_decomposed)


# %%
def checksum(defragmentized: list):
    checksum = 0
    for index in range(len(defragmentized)):
        value = defragmentized[index]
        if value != ".":
            mult = index * int(value)
            checksum += mult
            print(f"index={index} value={value} mult={mult} checksum={checksum}")
    return checksum


checksum_value = checksum(list_decomposed)
print(f"{checksum_value=}")

# %%
