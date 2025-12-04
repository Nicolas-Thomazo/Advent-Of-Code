# %%
from pathlib import Path

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

    # if "\n" in content_list[-1]:
    #     content_list[-1] = content_list[-1][:-1]
    return content_list


input = get_content(use_demo=True)
print(input)

# %%


def make_hash_map(string: str) -> dict:
    map_position = {}
    for index, char in enumerate(string):
        # print(f"{index=} {char=}")
        if int(char) in map_position:
            # print(f"append char {char}")
            map_position[int(char)].append(index)
        else:
            map_position[int(char)] = [index]
    return map_position


map_position = make_hash_map("818181911112111")
print(f"{map_position=}")
# %%
string = "818181911112111"
size_string: int = len(string)
battery_size = 12
max_possible_index = size_string - battery_size

batteries_result = []
map_position = make_hash_map(string)
queue = [9,8,7,6,5,4,3,2,1]

# for value in range(9, 0, -1):
for value in queue:
    if value in map_position:
        list_positions = map_position[value]
        new_list_pos = list_positions.copy()
        print(f"{value=} contains {list_positions}")
        for index_pos, position in enumerate(list_positions):
            if position < max_possible_index:
                batteries_result.append(string[position])
                max_possible_index += 1

                # new_list_pos.pop(index_pos)
                # map_position[value] = new_list_pos
                print(f"Append position to batterie {batteries_result}")
    else:
        print(f"No more in dict for {value=}")
        queue.remove(value)
# print(f"\n{batteries_result=}")
# print(f"{map_position=}")

# %%


# %%
sum_value = 0
for string in input:
    print(f"Input string={string}")
    first_max, second_max = get_joltage_batteries(string)
    print(f"Batteries={first_max}{second_max}")
    sum_value += int(str(first_max) + str(second_max))
print(f"Result={sum_value}")

# %%
