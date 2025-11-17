# %%

from pathlib import Path


def get_content(use_demo: bool) -> str:
    if use_demo:
        file = Path("input_example.txt")
    else:
        file = Path("input.txt")

    with open(file) as f:
        content = f.read()
    return content


def parse_input(input: str):
    input_list = input.split("\n")
    list_keys, list_equations = [], []
    for line in input_list:
        parsed_line = line.split(":")

        test_value = int(parsed_line[0])
        list_keys.append(test_value)

        equation = [int(x) for x in parsed_line[1].strip().split(" ")]
        list_equations.append(equation)

    return list_keys, list_equations


def compute(current_sum: int, operation: str, number: int):
    if operation == "+":
        return current_sum + number
    elif operation == "*":
        return current_sum * number
    else:
        raise ValueError("not supported")


def iterate(
    equation: list[int],
    key: int,
    index: int,
    current_sum: int | None = None,
    list_combinaisons: list[int] | None = None,
):
    if current_sum is None:
        current_sum = equation[0]

    if list_combinaisons is None:
        list_combinaisons = []

    if index == len(equation):
        list_combinaisons.append(current_sum)
        return list_combinaisons

    number = equation[index]

    for operation in ["+", "*"]:
        new_sum = compute(current_sum, operation, number)
        iterate(
            equation,
            key=key,
            index=index + 1,
            current_sum=new_sum,
            list_combinaisons=list_combinaisons,
        )
    return list_combinaisons


content = get_content(use_demo=False)
list_keys, list_equations = parse_input(content)

total_calibration = 0
for key, equation in zip(list_keys, list_equations):
    list_combinaisons = iterate(equation, key, index=1)

    if key in list_combinaisons:
        total_calibration += key

print(f"AOC Day 7 - part 1: result={total_calibration}")

# %%
