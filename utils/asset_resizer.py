from PIL import Image
import os

assets_path = "assets/"
assets_out_path = "assets_/"
if not os.path.isdir(assets_out_path):
    os.mkdir(assets_out_path)

for image in os.listdir(assets_path):
    try:
        img = Image.open(os.path.join(assets_path, image))
        print(img.size)
        img_ = img.resize((24, 24), resample=Image.BOX)
        img_.save(os.path.join(assets_out_path, image), "png")
    except IOError:
        print(f"invalid file {image}")