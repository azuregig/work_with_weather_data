# adapted from Sebastian Raschka, 2022 (https://github.com/rasbt/mnist-pngs)

import os
from PIL import Image, ImageFilter

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input_folder", type=str)
parser.add_argument("--output_folder", type=str)

args = parser.parse_args()


def emboss(file):
    with Image.open(file) as img:
        img.load()

    img_grey = img.convert('L')

    img_grey_smooth = img_grey.filter(ImageFilter.SMOOTH)

    emboss = img_grey_smooth.filter(ImageFilter.EMBOSS)

    return emboss
    
    img = img.filter(ImageFilter.EMBOSS)



if __name__ == "__main__":
    for file in os.listdir(args.input_folder):
        path = os.path.join(args.input_folder, file)
        output = emboss(path)
        output.save(os.path.join(args.output_folder, file.split(".")[0] + "_emboss.png"))

