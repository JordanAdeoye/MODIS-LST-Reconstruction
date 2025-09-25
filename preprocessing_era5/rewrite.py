from netCDF4 import Dataset, date2num
import os
import xarray as xr
import numpy as np 
import pandas as pd



def rewrite_func(input_dir,output_dir,var_name,temp_long_name):
    filenames=[f for f in os.listdir(input_dir) if f.endswith(".nc")]
    for file in filenames:
        filo=file.replace(".nc", "_rewrite.nc")
        file_path=os.path.join(input_dir, file)
        file_patho=os.path.join(output_dir, filo)
        data=xr.open_dataset(file_path)
        start_date=str(data.valid_time.values[0])
        end_date=str(data.valid_time.values[-1])
        dates = pd.date_range(start=start_date, end=end_date, freq="h")
        t_data=data[var_name].values
        lat_data=data.latitude.values
        lon_data=data.longitude.values
    
        with Dataset(file_patho, "w", format="NETCDF4") as nc_file:
            # Create dimensions
            nc_file.createDimension("time", len(dates)) 
            nc_file.createDimension("lat", len(lat_data))
            nc_file.createDimension("lon", len(lon_data))
        
            # Create coordinate variables
            times = nc_file.createVariable("time", "f8", ("time",))
            lat = nc_file.createVariable("lat", "f8", ("lat",))
            lon = nc_file.createVariable("lon", "f8", ("lon",))
        
            # Create variables
            t = nc_file.createVariable("t2m", "f8", ("time", "lat", "lon",))
        
            # Add attributes to coordinate variables
            times.units = "hours since 2001-01-01 00:00:00"
            times.calendar = "gregorian"
            lat.units = "degrees_north"
            lon.units = "degrees_east"
            lat.long_name = "Latitude"
            lon.long_name = "Longitude"
        
            # Add attributes to data variables
            t.units = "K"
            t.long_name = temp_long_name

            # Write data to coordinate variables
            times[:] = date2num(dates.to_pydatetime(), units=times.units, calendar=times.calendar)
            lat[:] = lat_data
            lon[:] = lon_data
        
            # Write data to data variables
            t[:, :, :] = t_data
        
        print(f"NetCDF file '{file_patho}' created successfully.")

# After REWRITING we use a command line tool function called cdo remapbil to spatial match the era5 data to modis