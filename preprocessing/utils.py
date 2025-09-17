from netCDF4 import Dataset, date2num
import xarray as xr
import os
import numpy as np
import pandas as pd
from pyhdf.SD import SD, SDC
from datetime import datetime, timedelta
import datetime

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



print(read_modis("MYD11A1.A2023001.h18v07.061.2023006121605.hdf","LST_Night_1km"))

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

# def LST_extraction(input_folder, var, qc_var, varo, output_folder):
#     os.makedirs(output_folder, exist_ok=True)
#     filenames=sorted([f for f in os.listdir(input_folder) if f.endswith(".hdf")])
#     for fil in filenames:
#         file=os.path.join(input_folder, fil)
#         output_path=os.path.join(output_folder, fil.replace(".hdf", ".nc"))
#         LST_1km     = read_modis(file, var).data
#         QC          = read_modis(file, qc_var).data
    
#     	ql1 = (QC.astype('uint8') & 0b00000011) >> 0 # Mandatory quality flag
#         ql2 = (QC.astype('uint8') & 0b00001100) >> 2 # Data quality flag
#         ql3 = (QC.astype('uint8') & 0b00110000) >> 4  # Emissivity error flag
#         ql4 = (QC.astype('uint8') & 0b01100000) >> 5 # LST error flag
    
#     	ql1_mask = np.where((ql1 == 0) | (ql1 == 1), 1, 0)
#         ql2_mask = np.where((ql2 == 0) | (ql2 == 1), 1, 0)
#         ql3_mask = np.where(ql3 == 0, 1, 0)
#         ql4_mask = np.where(ql4 == 0, 1, 0)
          
#         total_mask = (ql1_mask & ql2_mask & ql3_mask & ql4_mask).astype(int)
#         LST_1km_valid=LST_1km*total_mask
#         LST_1km_valid[LST_1km_valid==0]=np.nan
          
# 	lat, lon = inverse_maps(18, 7, 1200)
#         x_res=np.linspace(lon.min(), lon.max(), lon.shape[0])
#         y_res=np.linspace(lat.min(), lat.max(), lat.shape[0])
        
    
#         year=int(fil.split(".")[1][1:5])
#         doy=int(fil.split(".")[1][5:8])
#         time=datetime.datetime(year, 1, 1) + timedelta(days=doy - 1)
#         time_values=time
          
#         with Dataset(output_path, "w", format="NETCDF4") as nc_file:
#             nc_file.createDimension("time", 1)
#             nc_file.createDimension("lat", len(y_res))
#             nc_file.createDimension("lon", len(x_res))
            
#             # Create coordinate variables
#             times = nc_file.createVariable("time", "f4", ("time",))
#             lat = nc_file.createVariable("lat", "f4", ("lat",))
#             lon = nc_file.createVariable("lon", "f4", ("lon",))
            
#             # Create variables
#             variables = nc_file.createVariable(varo, "f4", ("time", "lat", "lon",))
            
#             # Add attributes to coordinate variables
#             times.units = "hours since 2001-01-01 00:00:00"
#             times.calendar = "gregorian"
#             lat.units = "degrees_north"
#             lon.units = "degrees_east"
#             lat.long_name = "Latitude"
#             lon.long_name = "Longitude"
            
#             # Add attributes to data variables
#             variables.units = "k"
#             variables.long_name = "Modis temperature"
            
#             # Write data to coordinate variables
#             times[:] = date2num(time_values, units=times.units, calendar=times.calendar)
#             lat[:] = y_res
#             lon[:] = x_res
            
#             # Write data to data variables
#             variables[:, :, :] = LST_1km_valid[::-1, :]
#         print(f"file {fil} processed and saved as {output_path}")