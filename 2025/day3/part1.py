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
    content_list = content_list[:-1]
    return content_list


input = get_content(use_demo=False)
print(input)

# %%


def get_joltage_batteries(string: str):
    list_battery = [int(x) for x in list(string)]
    print(f"{list_battery=}")
    xmax1 = np.argmax(list_battery[:-1])
    first_max = list_battery[xmax1]
    for i in range(0, xmax1 + 1):
        _ = list_battery.pop(0)

    xmax2 = np.argmax(list_battery)
    second_max = list_battery[xmax2]

    return first_max, second_max


# %%
sum_value = 0
for string in input:
    print(f"Input string={string}")
    first_max, second_max = get_joltage_batteries(string)
    print(f"Batteries={first_max}{second_max}")
    sum_value += int(str(first_max) + str(second_max))
print(f"Result={sum_value}")

# %%
