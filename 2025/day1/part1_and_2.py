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
    if content_list[-1] == "":
        content_list = content_list[:-1]
    return content_list


def rotate_dial(position: int, step: int, direction: str) -> tuple[int, int]:
    quotient: int = step // 100
    remainder: int = step % 100
    count = quotient
    prev_position = position
    if direction == "L":
        position -= remainder
        if position < 0 and position != 0:
            position += 100
            if prev_position != 0:
                count += 1
    else:
        position += remainder
        if position >= 100:
            position -= 100
            if prev_position != 0 and position != 0:
                count += 1

    if position == 0:
        count += 1
    return position, count


def find_password(
    dial_value: int, instructions: list[str], is_part_1: bool = True
) -> tuple[int, int]:
    count_full_loop = 0
    for instruc in instructions:
        direction: str = instruc[0]
        step = int(instruc[1:])
        dial_value, count_loop = rotate_dial(dial_value, step, direction)

        # Update full loop count based on puzzle (either the first part of the puzzle or the second)
        if is_part_1:
            if dial_value == 0:
                count_full_loop += 1
        else:
            count_full_loop += count_loop
        print(
            f"The dial is rotated {instruc} by pointing at {dial_value} -  0 loops: {count_loop}"
        )
    return count_full_loop, dial_value


INITIAL_DIAL_VALUE = 50
MAKE_PART_NUMBER_ONE = False

instructions = get_content(use_demo=False)
print(f"{instructions=}")
count_full_loop, result_dial_value = find_password(
    INITIAL_DIAL_VALUE, instructions, is_part_1=MAKE_PART_NUMBER_ONE
)
print(f"Dial value: {result_dial_value} and full loop count: {count_full_loop}")

# %%
