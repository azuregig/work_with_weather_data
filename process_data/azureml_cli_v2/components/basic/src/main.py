import os
import numpy as np
from PIL import Image

#import mlflow

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input_folder", type=str)
parser.add_argument("--output_folder", type=str)

args = parser.parse_args()

#mlflow.log_text(os.listdir(args.input_folder), "input_folder_contents.txt")

def convert(file):
    arr = np.genfromtxt(os.path.join(args.input_folder, file), delimiter=' ', dtype='str')
    #mlflow.log_metric("array_shape", arr.shape[0])
    print(arr.shape)
    
    imgdata = np.resize(arr,(32,32))
    img = Image.fromarray(imgdata.astype(np.uint8))

    img.save(os.path.join(args.output_folder, file.split(".")[0] + ".png"))

if __name__ == "__main__":

    for file in os.listdir(args.input_folder):
        convert(file)
    