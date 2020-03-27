import xarray as xr
import os
import numpy as np
import datetime
import glob
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

process_path = r"/home/knn/Desktop/wrf_umut_mgm/"
start = datetime.datetime.now()
for file_ in glob.glob1(process_path, "wrf_*.nc"):
    f_ = os.path.join(process_path, file_)
    print(file_)



file_ = r"/home/knn/Desktop/wrf_umut_mgm/wrf_20200214_00_2.nc"


# read data file
netcdf_data_file = xr.open_dataset(file_)




# Create latitude and longitude mesh for the given area of interest

lon, lat = np.meshgrid(netcdf_data_file.longitude.values, netcdf_data_file.latitude.values)
plt.figure(figsize=(6, 3))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_global()
ax.coastlines()

# Display data of interest
ax.contourf(lon, lat, netcdf_data_file.sf_0.values[0])
