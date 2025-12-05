# adapted from Sebastian Raschka, 2022 (https://github.com/rasbt/mnist-pngs)

import struct
import gzip
import os
import random
import urllib.request
import numpy as np
from PIL import Image

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--output_folder", type=str)
parser.add_argument("--sampling", type=float, default=1)
parser.add_argument("--dirs", type=str, default="true")    # no support for passing booleans in component parameters
#parser.add_argument("--dirs", action=argparse.BooleanOptionalAction, default=True) # specify --no-dirs to not create subfolders for each class

args = parser.parse_args()

urls = [
    "http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz",
    "http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz",
    "http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz",
    "http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz",
]
filenames = []

for url in urls:
    filename = os.path.basename(url)
    filename = os.path.join(".", filename)
    filename = filename.replace("t10k", "test")
    filenames.append(filename)
    urllib.request.urlretrieve(url, filename)


zipped_mnist = [f for f in os.listdir() if f.endswith("ubyte.gz")]
for z in filenames:
    with gzip.GzipFile(z, mode="rb") as decompressed, open(z[:-3], "wb") as outfile:
        outfile.write(decompressed.read())


def load_mnist(path, kind="train"):
    """Load MNIST data from `path`"""
    labels_path = os.path.join(path, f"{kind}-labels-idx1-ubyte")
    images_path = os.path.join(path, f"{kind}-images-idx3-ubyte")

    with open(labels_path, "rb") as lbpath:
        magic, n = struct.unpack(">II", lbpath.read(8))
        labels = np.fromfile(lbpath, dtype=np.uint8)

    with open(images_path, "rb") as imgpath:
        magic, num, rows, cols = struct.unpack(">IIII", imgpath.read(16))
        images = np.fromfile(imgpath, dtype=np.uint8).reshape(len(labels), 784)

    return images, labels


image_name_counter = 0

for kind in ("train", "test"):
    if args.dirs == "true":
        if not os.path.isdir(os.path.join(args.output_folder, kind)):
            os.mkdir(os.path.join(args.output_folder, kind))
        for i in range(10):
            if not os.path.isdir(os.path.join(args.output_folder, kind, str(i))):
                os.mkdir(os.path.join(args.output_folder, kind, str(i)))

    images, labels = load_mnist(path=".", kind=kind)

    for image, label in zip(images, labels):
        image = image.reshape(28, 28)
        name = f"{image_name_counter}.png"
        image_name_counter += 1
 
        im = Image.fromarray(image)

        if args.dirs == "true":
            path = os.path.join(args.output_folder, kind, str(label), name)
        else:
            path = os.path.join(args.output_folder, name)


        # create pngs of all files only if args.sampling is 1
        # otherwise, randomly sample args.sampling percent of the files
        if random.random() < args.sampling:
            im.save(path)