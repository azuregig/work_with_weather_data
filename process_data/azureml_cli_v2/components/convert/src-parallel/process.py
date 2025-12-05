# adapted from Sebastian Raschka, 2022 (https://github.com/rasbt/mnist-pngs)

import os
from PIL import Image, ImageFilter

import argparse


def init():
    global args

    parser = argparse.ArgumentParser()
    parser.add_argument("--output_folder", type=str)

    args = parser.parse_args()
    

def emboss(file):
    with Image.open(file) as img:
        img.load()

    img_grey = img.convert('L')

    img_grey_smooth = img_grey.filter(ImageFilter.SMOOTH)

    emboss = img_grey_smooth.filter(ImageFilter.EMBOSS)

    return emboss


def run(mini_batch):
    resultslog = []
    for file in mini_batch:
        print(type(file))
        print(file)
        output = emboss(file)
        output.save(os.path.join(args.output_folder, file.split(".")[0] + "_emboss.png"))

        resultslog.append(os.path.join(args.output_folder, file.split(".")[0] + "_emboss.png"))
    return resultslog


# foo


