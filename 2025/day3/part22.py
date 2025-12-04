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
def get_list_max_joltage(string):
    battery_size = 11
    until = -battery_size

    list_battery: list[int] = [int(x) for x in list(string)]
    print(f"{list_battery=}")
    list_max = []
    # Get max for availables string
    xmax = 0
    for _ in range(0, 12):
        list_battery = list_battery[xmax:]
        if until == 0:
            new_xmax = int(np.argmax(list_battery))
        else:
            new_xmax = int(np.argmax(list_battery[:until]))
        first_max = list_battery[new_xmax]
        print(f"{first_max=}  from {xmax=} to {until=} {list_battery[:until]}")
        until += 1
        # list_battery.remove(first_max)
        list_max.append(first_max)
        xmax = new_xmax + 1
    print(f"{list_max=}")
    return list_max


# %%

sum_value = 0
for string in input:
    list_max = get_list_max_joltage(string)
    max_string = "".join([str(x) for x in list_max])
    sum_value += int(max_string)
print(f"Result={sum_value}")
# %%
