# %%
import glob

from PIL import Image


def make_gif(frame_folder):
    frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.png")]
    frame_one = frames[0]
    frame_one.save(
        "2025/day9/day9_solution.gif",
        format="GIF",
        append_images=frames,
        save_all=True,
        duration=1,
        loop=0,
    )


make_gif(frame_folder="2025/day9/images/")

# %%
