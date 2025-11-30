# %%
from collections import deque
from pathlib import Path

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
    list_decomposed = []
    index_file = 0
    for index_input in range(len(input)):
        char = input[index_input]
        value = int(char)
        if index_input % 2 == 0:
            for _ in range(value):
                decomposed.append(index_file)
                list_decomposed.append(index_file)
            index_file += 1
        else:
            liste_dot = ["."] * value
            list_decomposed.extend(liste_dot)
    return decomposed, list_decomposed


deque_decomposed, list_decomposed = decompose_queue(input)
print(f"{deque_decomposed=}")
print(f"{list_decomposed=}")
# %%

defragmentized = []
for elem in list_decomposed:
    if len(deque_decomposed) == 0:
        print("Finish dequeue empty")
        break
    if elem != ".":
        deque_decomposed.popleft()
        defragmentized.append(int(elem))
    else:
        value = deque_decomposed.pop()
        defragmentized.append(int(value))
print(f"{defragmentized=}")


# %%
def checksum(defragmentized: list):
    checksum = 0
    for index in range(len(defragmentized)):
        value = defragmentized[index]
        mult = index * int(value)
        checksum += mult
        print(f"index={index} value={value} mult={mult} checksum={checksum}")
    return checksum


checksum_value = checksum(defragmentized)
print(f"{checksum_value=}")

# %%
