import xarray as xr
import os
import numpy as np
import datetime
import glob
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import rioxarray

start = datetime.datetime.now()

process_path = r"/home/knn/Desktop/wrf_umut_mgm/"


def read_wrf_data(f, export=False):
    # read data file
    netcdf_data_file = xr.open_dataset(f)

    # Create latitude and longitude mesh for the given area of interest

    lon, lat = np.meshgrid(netcdf_data_file.longitude.values, netcdf_data_file.latitude.values)
    plt.figure(figsize=(6, 3))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()
    ax.coastlines()

    # Display data of interest
    ax.contourf(lon, lat, netcdf_data_file.sf_0.values[0])
    if export:
        print("Y")


for file_ in glob.glob1(process_path, "wrf_*.nc"):
    try:
        f_ = os.path.join(process_path, file_)
        print("Reading the", file_, "file")
        read_wrf_data(f_, export=True)
    except:
        pass


end = datetime.datetime.now()
print(end - start)
