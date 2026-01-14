# %%
import glob

import numpy as np
from PIL import Image


def sort_images(frame_folder):
    liste_images = []
    for image in glob.glob(f"{frame_folder}/*.png"):
        liste_images.append(image)
    liste_number = []
    for x in liste_images:
        index = x.split("images/ploygon_")[1].split(".png")[0]
        liste_number.append(int(index))
    arr_index = np.argsort(liste_number)
    arr_sorted = np.array(liste_images)[arr_index]
    return list(arr_sorted)

def make_gif(frame_folder):
    liste_images = sort_images(frame_folder)
    frames = [Image.open(image) for image in liste_images]
    frame_one = frames[0]
    frame_one.save(
        "day9_solution.gif",
        format="GIF",
        append_images=frames,
        save_all=True,
        duration=0.01,
        loop=0,
    )


make_gif(frame_folder="images/")

# %%
