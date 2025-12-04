# %%
import math
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


def check_one_combination_repeat(number_digits: int, size: int, string: str):
    id_invalid = None
    quotient = size // number_digits
    # print(f"{quotient=} for {number_digits}")
    is_not_equal = False
    # list_sub_ids=[]
    for i in range(quotient - 1):
        coef = number_digits * i
        borne_min = coef
        borne_max = number_digits + coef

        coef2 = number_digits * (i + 1)
        borne_min2 = coef2
        borne_max2 = number_digits + coef2

        val1 = string[borne_min:borne_max]
        val2 = string[borne_min2:borne_max2]
        # print(f"{val1=} {val2=}")
        # list_sub_ids.extend([val1,val2])
        if val1 != val2:
            is_not_equal = True
            # print("Condition not repeated")
            break
    # id_invalid=int(str(val1)+str(val2))
    id_invalid = string
    return is_not_equal, id_invalid


def check_all_combination(string: str):
    size = len(string)
    is_not_equal = True
    low_index = 1
    max_index = math.floor(size / 2) + 1
    id_invalid = None
    for number_digits in range(low_index, max_index):
        if size % number_digits == 0:
            is_not_equal, id_invalid = check_one_combination_repeat(
                number_digits, size, string
            )
            if not is_not_equal:
                break
    return id_invalid, is_not_equal


list_invalid_ids = []
for elem in input:
    list_range = elem.split("-")
    range_low, range_high = int(list_range[0]), int(list_range[1])
    # print("*" * 10, f"from {range_low} to {range_high}", "*" * 10)
    for value in range(range_low, range_high + 1):
        id_invalid, is_not_equal = check_all_combination(str(value))
        if not is_not_equal:
            list_invalid_ids.append(int(id_invalid))
print(f"{list_invalid_ids=}")
print(f"The sum of invalid ids={sum(list_invalid_ids)}")
# %%
