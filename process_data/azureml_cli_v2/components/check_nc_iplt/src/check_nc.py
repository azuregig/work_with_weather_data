import argparse
import os
import mlflow

import cartopy.crs as ccrs
import iris
import iris.plot as iplt
import matplotlib.pyplot as plt
import time

parser = argparse.ArgumentParser()
parser.add_argument("--nc_folder", type=str)
parser.add_argument("--nc_filename", type=str)

args = parser.parse_args()


def iris_plot(nc_file):
    '''
    This function takes an .nc file or other gridded file format that is readable by the iris library.
    It logs diagnostic information about this cube to the run log using mlflow.
    It does not read in or write out the full cube data (check what iplt actually does here?)
    '''

    # record the provided input parameter to the run log
    mlflow.log_param('cube', nc_file)

    # load the cube object into memory. Note: Iris does not necessarily load the data until you call cube.data
    cube = iris.load_cube(nc_file)

    mlflow.log_metric('has_lazy_data', int(cube.has_lazy_data()), step=0)

    mlflow.log_metric('dimensions', len(cube.shape))
    mlflow.log_dict(cube.attributes, "cube_attributes.json")
    summary = cube.summary(shorten=False, name_padding=35)
    print(cube.has_lazy_data())
    mlflow.log_metric('has_lazy_data', int(cube.has_lazy_data()), step=1)

    # the outputs directory is available by default for outputs that should be uploaded to the run log at the end of the run
    #with open('outputs/cube_summary.txt', 'w') as f:
    #    f.write(summary)

    # to make an artifact available in the run log *during* the run, use mlfow:
    #mlflow.log_artifact('outputs/cube_summary.txt', "cube_summary.txt")

    mlflow.log_text(summary, "cube_summary.txt")

    # create a figure object that will allow us to log a diagnostic figure with mlflow
    fig = plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree())
    # ax = plt.axes(projection=ccrs.Stereographic())
    # iplt.pcolormesh(cube.extract(realization=16, time=...))
    iplt.pcolormesh(cube[0])
    print(cube.has_lazy_data())
    mlflow.log_metric('has_lazy_data', int(cube.has_lazy_data()), step=2)

    data = cube.data
    mlflow.log_metric('has_lazy_data', int(cube.has_lazy_data()), step=3)
    #print(data.shape)
    #mlflow.log_metric('has_lazy_data', int(cube.has_lazy_data()), step=4)



    ax.coastlines()
    #plt.savefig('plot.png')

    #plt.show()
    mlflow.log_figure(fig, f'plot.png')
    mlflow.log_metric('has_lazy_data', int(cube.has_lazy_data()), step=5)




def main(args):
    iris_plot(os.path.join(args.nc_folder, args.nc_filename))



if __name__ == "__main__":
    main(args)
