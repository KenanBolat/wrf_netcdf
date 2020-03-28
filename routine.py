import xarray as xr
import os
import numpy as np
import datetime
import glob
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import rioxarray
import osr
import gdal

start = datetime.datetime.now()

process_path = r"/home/knn/Desktop/wrf_umut_mgm/"


def read_wrf_data(f, export=False):
    # read data file
    netcdf_data_file = xr.open_dataset(f)
    # aa = xr.open_dataset(f)
    # bb = aa.sf_0.assign_coords(longitude=aa.longitude, latitude=aa.latitude)
    # cc = bb.rio.set_crs(4326)
    # dd = cc.rio.set_spatial_dims("longitude", "latitude")
    lon, lat = np.meshgrid(netcdf_data_file.longitude.values, netcdf_data_file.latitude.values)
    plt.figure(figsize=(6, 3))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()
    ax.coastlines()

    # Display data of interest
    ax.contourf(lon, lat, netcdf_data_file.sf_0.values[0])
    if export:
        print("Exporting .. ", f)
        conversion_data = {
            "WRF": [(6.8444164, 0.02704, 0.0, 50.707482, 0.0, -0.02704), (816, 1690), [50.693962, 6.8308964],
                    [28.65548, 52.505104]]}

        # Save as Geotiff
        transform = conversion_data['WRF']
        epsg_code = 4326
        projection = osr.SpatialReference()
        projection.SetWellKnownGeogCS("EPSG:" + str(epsg_code))
        driver = gdal.GetDriverByName("GTiff")
        export_data = driver.Create(os.path.basename(f).split(".")[0] + ".tiff", transform[1][1], transform[1][0], 1,
                                    gdal.GDT_Float32)
        # sets the extend
        export_data.SetGeoTransform(transform[0])
        # sets projection
        export_data.SetProjection(projection.ExportToWkt())

        # TODO check xarray datastoring mechanism
        #
        # export_data.GetRasterBand(1).WriteArray(
        #     np.rot90(np.rot90(np.transpose(np.rot90(netcdf_data_file.sf_0.values[0])))))

        export_data.GetRasterBand(1).WriteArray(np.fliplr(np.flipud(np.fliplr(netcdf_data_file.sf_0.values[0]))))
        # if you want these values transparent
        export_data.GetRasterBand(1).SetNoDataValue(999)
        # Save the data
        export_data.FlushCache()
        # Create latitude and longitude mesh for the given area of interest

        print("Exporting Done..")


for file_ in glob.glob1(process_path, "wrf_*.nc"):
    try:
        f_ = os.path.join(process_path, file_)
        print("Reading the", file_, "file")
        read_wrf_data(f_, export=True)
    except:
        print("There is a problem with the process")

end = datetime.datetime.now()
print(end - start)
