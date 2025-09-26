from netCDF4 import Dataset, date2num
import xarray as xr
import os
import shutil
import rioxarray
import numpy as np
import pandas as pd
from pyhdf.SD import SD, SDC
import matplotlib.pyplot as plt
import geopandas as gpd
import regionmask
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from matplotlib.ticker import MultipleLocator
from datetime import datetime, timedelta
import datetime
import time
from scipy.interpolate import interp1d
from joblib import Parallel, delayed


def read_modis(file_path, var_name):
    hdf_file = SD(file_path, SDC.READ)
    data_obj = hdf_file.select(var_name)
    attrs=data_obj.attributes()
    data=data_obj[:]
    fillvalues=attrs.get("_FillValue", None)
    scale_factor=attrs.get("scale_factor", 1.0)
    offset=attrs.get("add_offset", 0.0)
    data=data*scale_factor+offset
    if fillvalues is not None:
        data=np.ma.masked_where(data_obj[:]==fillvalues, data)
    return data

def inverse_maps(H,V,size):
    Lat=np.zeros((size,size))
    Lon=np.zeros((size,size))
    R=6371007.181
    T = 1111950
    xmin = -20015109.
    ymax = 10007555.
    w = T /size
    y=np.array([(ymax-(i+.5)*w-V*T) for i in range(size)] )
    x =np.array([((j+.5)*w + (H)*T + xmin) for j in range(size)])
    for i, yy in enumerate(y):
        for j, xx in enumerate(x):
            ll=yy/R
            Lat[i,j]=ll*180/np.pi
            Lon[i,j]=180/np.pi*(xx/(R*np.cos(ll)))
    return Lat, Lon



def Era_interpolation(input_folder, era5_file_path, output_folder, view_time='Day', n_jobs=8):
    filenames = sorted([f for f in os.listdir(input_folder) if f.endswith(".hdf")])

    for fil in filenames:  # For testing, one file
        file = os.path.join(input_folder, fil)

        # Read MODIS view time
        view_time_data = read_modis(file, f"{view_time}_view_time").data
        year = int(fil.split(".")[1][1:5])
        doy = int(fil.split(".")[1][5:8])
        base_time = datetime.datetime(year, 1, 1) + timedelta(days=doy - 1)

        # Create pixel-level UTC time 
        lat, lon = inverse_maps(18, 7, 1200)
        view_time_UTC = view_time_data - lon / 15
        time_offsets = view_time_UTC.astype("timedelta64[h]")
        time_UTC = np.datetime64(base_time) + time_offsets

        # Define time range for ERA5 
        time_min = time_UTC.min() - np.timedelta64(4, "h")
        time_max = time_UTC.max() + np.timedelta64(4, "h")

        # Load ERA5 subset
        data = xr.open_dataset(era5_file_path)
        skt = data["t2m"].sel(time=slice(time_min, time_max))

        # Interpolation step using nearest
        unique_times = np.unique(time_UTC)

        def interpolate_group(t):
            mask = (time_UTC == t)
            try:
                skt_slice = skt.sel(time=t, method="nearest").values
            except KeyError:
                return np.full(mask.shape, np.nan, dtype=np.float32)
            result = np.full(mask.shape, np.nan, dtype=np.float32)
            result[mask] = skt_slice[mask]
            return result

        print(f"Interpolating {len(unique_times)} time groups...")
        results = Parallel(n_jobs=n_jobs)(delayed(interpolate_group)(t) for t in unique_times)

        interp_array = np.nanmean(results, axis=0)

        # === Write interpolated result to NetCDF ===
        output_path = os.path.join(output_folder, fil.replace(".hdf", "_2m_interp.nc"))
        x_res = np.linspace(lon.min(), lon.max(), lon.shape[1])
        y_res = np.linspace(lat.min(), lat.max(), lat.shape[0])
        time_value = base_time

        with Dataset(output_path, "w", format="NETCDF4") as nc_file:
            nc_file.createDimension("time", 1)
            nc_file.createDimension("lat", len(y_res))
            nc_file.createDimension("lon", len(x_res))

            # Coordinate variables
            times = nc_file.createVariable("time", "f4", ("time",))
            lat_var = nc_file.createVariable("lat", "f4", ("lat",))
            lon_var = nc_file.createVariable("lon", "f4", ("lon",))

            # Data variable
            skt_var = nc_file.createVariable("2m_interp", "f4", ("time", "lat", "lon",))

            # Attributes
            times.units = "hours since 2001-01-01 00:00:00"
            times.calendar = "gregorian"
            lat_var.units = "degrees_north"
            lon_var.units = "degrees_east"
            lat_var.long_name = "Latitude"
            lon_var.long_name = "Longitude"
            skt_var.units = "K"
            skt_var.long_name = "Interpolated ERA5 2m temperature"

            # Write data
            times[:] = date2num(time_value, units=times.units, calendar=times.calendar)
            lat_var[:] = y_res
            lon_var[:] = x_res
            skt_var[0, :, :] = interp_array[::-1, :]  # Flip latitude

        print(f"File {fil} processed and saved as {output_path}")