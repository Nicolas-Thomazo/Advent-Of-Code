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
    content_list: list[str] = content.split(",")
    if "\n" in content_list[-1]:
        content_list[-1] = content_list[-1][:-1]
    return content_list


input = get_content(use_demo=False)
print(input)


# %%
def check_repeat(input_string: str):
    invalid_id = None
    count_char = len(str(input_string))
    is_repeated = False
    if count_char % 2 == 0:
        split_index = int(count_char / 2)
        val1 = int(input_string[:split_index])
        val2 = int(input_string[split_index:])
        if val1 == val2:
            is_repeated= True
            invalid_id = int(str(val1)+str(val2))
    # if is_repeated:
    #     print(f"For {input_string=}: {is_repeated=} value repeat: {val1}")
    return is_repeated,invalid_id


# check_repeat("2121221212")
# %%
sum_repeat = 0
count_repeat = 0
for elem in input:
    list_range = elem.split("-")
    range_low, range_high = int(list_range[0]), int(list_range[1])
    for value in range(range_low, range_high+1):
        is_repeated, repetead_value = check_repeat(str(value))
        if is_repeated:
            count_repeat += 1
            sum_repeat += repetead_value

print(f"Number of repeated values {count_repeat} and {sum_repeat=}")
# %%
