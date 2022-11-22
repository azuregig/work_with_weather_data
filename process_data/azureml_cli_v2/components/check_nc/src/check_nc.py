import argparse

import os
import matplotlib.pyplot as plt
import mlflow
import numpy as np
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset

parser = argparse.ArgumentParser()
parser.add_argument("--nc_folder", type=str)
parser.add_argument("--nc_filename", type=str)
parser.add_argument("--plot_var", type=str)

args = parser.parse_args()

def check_nc(nc_file):
    data = Dataset(nc_file, mode='r') # read the data 
    variables = list(data.variables.keys()) # print the variables in the data

    params = {
        "filetype": type(data),
        "num_vars": len(variables),
        "variables": list(data.variables.keys())
    }


    data.close()
    
    #print(params)
    mlflow.log_params(params)

# from https://joehamman.com/2013/10/12/plotting-netCDF-data-with-Python
def plot_on_map(nc_file, plot_var):
    fh = Dataset(nc_file, mode='r') # read the data 

    lons = fh.variables['longitude'][:]
    lats = fh.variables['latitude'][:]
    Temp = fh.variables[plot_var][:]
    p = fh.variables['forecast_period'][:]

    temp_units = fh.variables[plot_var].units

    fh.close()

    # Get some parameters for the Stereographic Projection
   # lon_0 = lons.mean()
    #lat_0 = lats.mean()
    lon_0 = -60
    lat_0 = -25
    
    fig = plt.figure()

    m = Basemap(width=10000000,height=7000000,
            resolution='l',projection='stere',\
            lat_ts=40,lat_0=lat_0,lon_0=lon_0)

    # Because our lon and lat variables are 1D,
    # use meshgrid to create 2D arrays
    # Not necessary if coordinates are already in 2D arrays.
    lon, lat = np.meshgrid(lons, lats)
    xi, yi = m(lon, lat)

    # Plot Data
    for i in range(0,Temp.shape[0]):
        temp = Temp[i,:,:]
        cs = m.pcolor(xi,yi,np.squeeze(temp), vmin=270, vmax=300)

        # Add Grid Lines
        m.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=10)
        m.drawmeridians(np.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=10)

        # Add Coastlines, States, and Country Boundaries
        m.drawcoastlines()
        m.drawstates()
        m.drawcountries()

        # Add Colorbar
        cbar = m.colorbar(cs, location='bottom', pad="10%")
        cbar.set_label(temp_units)

        # Add Title
        plt.title(f'Surface temperature - {p[i]}')

        # Save locally - use for testing only
        #plt.savefig(f'plot_{i}.png')

        # Save to an output location - define a component output location to use this
        #plt.savefig(os.path.join(args.<outputloc>, f'plot_{i}.png')

        # Log to the run
        mlflow.log_figure(fig, f'surface_temperature_{p[i]}.png')

def main(args):
    check_nc(os.path.join(args.nc_folder, args.nc_filename))
    plot_on_map(os.path.join(args.nc_folder, args.nc_filename), args.plot_var)


if __name__ == "__main__":
    main(args)
