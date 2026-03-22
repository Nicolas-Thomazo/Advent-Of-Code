# %%
# Alorithme utilisé: BFS (Breadth First Search)
# 1. On convertit le joltage attendu en binaire: .##. ==> 0110 ==> 6 en décimal
# 2. On convertit les boutons en entier. Le bouton (0,2) ==> 1010 en binaire ==> 10 en décimal.
# 3. Appuyer sur le bouton
#   - L'operation d'appuyer sur un bouton correspond à executer une operation XOR entre le boutton et le joltage actuel.
#   - Par exemple, si le joltage actuel est 1100 et que le bouton est 1010, nouveau joltage = 1100 XOR 1010 = 0110
#   - Comme on utilise des décimals on peut appliquer l'opération entre les déciamls: nouveau joltage = 12 XOR 10 = 6 (qui est bien égale à 0110)
# 4. Il faut maintenant tester les différentes combinaisons de boutons pour atteindre le joltage attendu.
#    On applique le BFS:
#     - On ajoute dans une queue le joltage initial 0 et le nombre de boutons pressés 0
#     - On à une boucle while tant que la queue n'est pas vide et que la solution n'est pas trouvé
#     - On pop le premier élément de la queue
#     - On applique les boutons un par un pour trouver le nouveau joltage
#     - On ajoute le nouveau joltage dans la queue si il n'a pas déjà été visité et on incrémente le nombre de boutons pressés
#     - Si le nouveau joltage est égal au joltage attendu, on a trouvé la solution et on peut sortir de la boucle while
# 5. On somme le nombre de boutons pressés pour chaque machine pour obtenir le résultat final.

import re
from collections import deque
from pathlib import Path

######################
#### Initialise ######
######################


def get_content(use_demo: bool) -> list[str]:
    print("*" * 50, "Import Data", "*" * 50)
    if use_demo:
        file = Path("input_example.txt")
    else:
        file = Path("input.txt")
    with open(file) as f:
        content: str = f.read()
    list_content: list[str] = content.split(sep="\n")
    if list_content[-1] == "":
        list_content.pop()
    return list_content


########################
####### Cast to int ####
########################


def joltage_to_binary(joltage: str) -> str:
    joltage_binary = ""
    for x in joltage:
        if x == ".":
            joltage_binary += "0"
        else:
            joltage_binary += "1"
    return joltage_binary


def binary_to_int(joltage_binary: str) -> int:
    return int(joltage_binary, base=2)


################################
####### Read & format input ####
################################


def button_to_int(one_button: str, size_output: int) -> int:
    """
    Transform the button in integer. Each button is represented by a tuple of two integers,
    which correspond to the index of the button that we want to press.

    For example if we have one_button = "(2,1)", we want to get the integer that corresponds to the
    binary number 101, which is 5 in decimal. We can do this by using the bitwise OR operator.
    - 2 corresponds to the binary number 010
    - 1 corresponds to the binary number 001
    - 2 | 1 corresponds to the binary number 011, which is 3 in decimal.

    Args:
    one_button (str): string that corresponds to the button, for example "(2,1)"

    Returns:
    int: integer that corresponds to the button, for example 3 correspond to 011 in binary.
    """
    list_buttons = one_button[1:-1].split(",")
    list_buttons = [int(x) for x in list_buttons]
    # print(f"{list_buttons=}")
    list_binary = []
    for idx_button in list_buttons:
        binary = ["0"] * size_output
        binary[idx_button] = "1"
        binary_string = "".join(binary)
        # print(f"{binary_string=} for button {idx_button}")
        list_binary.append(int(binary_string, base=2))
    # print(f"{list_binary=}")
    final_button = None
    for x in list_binary:
        # print(x,":","{0:04b}".format(x))
        if final_button is None:
            final_button = x
        else:
            final_button = final_button | x
    # print(f"Button: {one_button} -> Transform in:", "{0:04b}".format(final_button))
    assert isinstance(final_button, int), (
        f"button should be an integer and is {type(final_button)}"
    )
    return final_button


def cast_buttons_to_int(list_buttons_one_line: list[str], joltage: str) -> list[int]:
    """Cast the list of buttons in integer. Each button is represented by a tuple of one or two integers."""
    list_buttons = []
    for button_set in list_buttons_one_line:
        button_value: int = button_to_int(button_set, len(joltage))
        list_buttons.append(button_value)
    return list_buttons


def format_input(
    list_lines: list[str],
) -> tuple[list[int], list[str], list[list[str]], list[list[int]]]:
    """
    Format the input to get the expected joltage and the list of buttons for each machine.
    The expected joltage is represented by a binary number, where 1 corresponds to a lit LED and 0 corresponds to an unlit LED.
    The buttons are represented by integers, where each integer corresponds to a combination of LEDs that will be toggled when the button is pressed.

    Args:
    list_lines (list[str]): list of lines from the input file, where each line corresponds to a machine and contains the expected joltage and the list of buttons.

    Returns:
    tuple[list[int], list[list[int]]]: a tuple containing the list of expected joltages and the list of buttons for each machine.
    """

    list_expected_joltages: list[int] = []
    list_buttons_str: list[list[str]] = []
    list_joltags_str = []
    list_buttons_int: list[list[int]] = []
    for i, line in enumerate(list_lines):
        regex_match = r"\[.*\]"
        find = re.search(regex_match, line)
        if not find:
            raise ValueError(f"Couldn't parse properly the input {line}")

        # Get the joltage and convert it to binary and then to integer
        array = find.group()[1:-1]
        joltage: str = joltage_to_binary(array)
        list_joltags_str.append(joltage)
        joltage_int = binary_to_int(joltage)
        list_expected_joltages.append(joltage_int)

        # Get the buttons and convert it to integer
        match_number_or_comma = r"[\d|,]+"
        list_buttons_one_machine: list[str] = re.findall(
            rf"\({match_number_or_comma}\)",
            line,
        )
        list_buttons_str.append(list_buttons_one_machine)
        temporary_list_buttons: list[int] = cast_buttons_to_int(
            list_buttons_one_machine, joltage
        )
        list_buttons_int.append(temporary_list_buttons)
    return (
        list_expected_joltages,
        list_joltags_str,
        list_buttons_str,
        list_buttons_int,
    )


########################
####### Flip button ####
########################


def apply_xor(curent_joltage: int, pressed_button: int) -> int:
    """
    Apply joltage with XOR operation

    Args:
    curent_joltage (list[int]): current joltage
    pressed_button (tuple): button to press

    Returns:
    list[int]: updated joltage
    """
    new_joltage: int = curent_joltage ^ pressed_button
    return new_joltage


def int_to_binary(value: int):
    return "{:b}".format(value)


########################
########## BFS #########
########################


def implement_bfs(buttons: list[int], joltage: int) -> int:
    """
    Implement BFS to find the minimum number of button presses to reach the expected joltage.
    We start from the initial joltage (0) and we apply the buttons one by one, until we reach the expected joltage.
    We keep track of the visited joltages to avoid infinite loops.

    Args:
        buttons (list[int]): list of buttons to press, where each button is represented by an integer that corresponds to a combination of LEDs that will be toggled when the button is pressed.
        joltage (int): expected joltage that we want to reach, represented by an integer that corresponds to a binary number, where 1 corresponds to a lit LED and 0 corresponds to an unlit LED.

    Returns:
        int: the minimum number of button presses to reach the expected joltage.
    """
    init_joltage = 0
    steps = 0
    queue = deque([(init_joltage, steps)])
    visited = set()
    solution = False
    while queue and not solution:
        current_joltage, current_steps = queue.popleft()
        current_steps += 1
        for button in buttons:
            new_joltage = apply_xor(current_joltage, button)
            if new_joltage == joltage:
                solution = True
                break
            if new_joltage not in visited:
                visited.add(new_joltage)
                queue.append((new_joltage, current_steps))
    assert solution, "A solution should have been found"
    return current_steps


list_lines: list[str] = get_content(use_demo=True)
list_joltages, list_joltags_str, list_buttons_str, list_buttons_int = format_input(
    list_lines
)
print("---------------- Joltage and buttons -----------------")
index = 0
while index < 3:
    print(
        list_joltages[index],
        ":",
        list_joltags_str[index],
        list_buttons_str[index],
        ["{:b}".format(button) for button in list_buttons_int[index]],
    )
    index += 1


print("---------------- Use BFS -----------------")
list_pressed_buttons = []
for joltage, buttons in zip(list_joltages, list_buttons_int):
    number_pressed_buttons = implement_bfs(buttons, joltage)
    list_pressed_buttons.append(number_pressed_buttons)

print("result is ", sum(list_pressed_buttons))  # 897 To high


# %%
