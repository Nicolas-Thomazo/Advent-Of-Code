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
    if content_list[-1] == "":
        content_list = content_list[:-1]
    return content_list

input=get_content(use_demo=False)
print(input)
# %%
matrix=None
for line in input:
    if matrix is None:
        matrix=np.array(list(line))
    else:
        array=np.array(list(line))
        matrix=np.vstack((matrix,array))
print(f"{matrix=}")

# %%
assert isinstance(matrix,np.ndarray)

def count_bouding_values(matrix,i,j):
    count_roll_paper=0
    for x in [-1,0,1]:
        for y in [-1,0,1]:
            is_not_center = (x,y)!=(0,0)
            is_au_bord = x+i<0 or x+i >=matrix.shape[0]
            is_au_bord_y = y+j<0 or y+j >=matrix.shape[1]
            if is_not_center and not is_au_bord and not is_au_bord_y:
                if matrix[x+i][y+j]=="@":
                    count_roll_paper+=1
            # if is_au_bord or is_au_bord_y:
                # print(f"Au bord {x+i=} {y+j=}")
    return count_roll_paper

count_roll_pape=count_bouding_values(matrix,0,0)
print(f"{count_roll_pape=}")
#%%
roll_paper_valid= 0

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        if matrix[i][j]=="@":
            count_roll_paper=count_bouding_values(matrix,i,j)
            if count_roll_paper<4:
                roll_paper_valid+=1
                print(f"One more paper valid at {i=} {j=}")
print(f"{roll_paper_valid=}")

# %%
