import os
import sys

import mlflow

# Must be imported before Iris!
import iris_sample_data
import iris

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--src_cube", type=str)
parser.add_argument("--grid_cube", type=str)
parser.add_argument("--output_folder", type=str)
parser.add_argument("--output_name", type=str)


args = parser.parse_args()


def regrid(src_dataset, base_dataset, storage_path, storage_name):
    # Load datasets as Iris cubes from sample data helper function.
    #src_cube = iris.load_cube(iris.sample_data_path("GloSea4", src_dataset_name))
    src_cube = iris.load_cube(src_dataset)
    #grid_cube = iris.load_cube(iris.sample_data_path("air_temp.pp"))
    grid_cube = iris.load_cube(base_dataset)

    # Linear regrid the source cube onto the grid provided by the grid cube.
    regrid_cube = src_cube.regrid(grid_cube, iris.analysis.Linear())

    # Save the regridded cube.
    iris.save(regrid_cube, os.path.join(storage_path, storage_name))


def main(args):
    regrid(args.src_cube, args.grid_cube, args.output_folder, args.output_name)


if __name__ == "__main__":
    main(args)

### python src/regrid.py --src_cube ./test/input/GloSea4/ensemble_000.pp --grid_cube ./test/input/air_temp.pp --output_file ./test/output/regridded.nc 