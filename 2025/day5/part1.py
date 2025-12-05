# %%
from pathlib import Path

######################
#### Initialise ######
######################


def get_content(use_demo: bool):
    print("*" * 50, "Import Data", "*" * 50)
    if use_demo:
        file = Path("input_example.txt")
    else:
        file = Path("input.txt")

    with open(file) as f:
        content: str = f.read()
    liste_ingredients = content.split("\n\n")

    fresh_ingredients = liste_ingredients[0].split("\n")
    available_ingredients = liste_ingredients[1].split("\n")[:-1]
    available_ingredients = [int(x) for x in available_ingredients]
    list_fresh_ingredients = []
    for fresh in fresh_ingredients:
        range_values = fresh.split("-")
        first, last = int(range_values[0]), int(range_values[1])
        list_fresh_ingredients.append((first, last))
    return list_fresh_ingredients, available_ingredients


fresh_ingredients, available_ingredients = get_content(use_demo=False)
print(f"{fresh_ingredients=}\n{available_ingredients=}")
# %%
count_fresh = 0
for ingredient in available_ingredients:
    for first, last in fresh_ingredients:
        if ingredient >= first and ingredient <= last:
            count_fresh += 1
            break
print(f"{count_fresh}")

# %%
