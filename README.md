download_modis -> download the data

# include image og how is looks ehen download 001 002
# then after you unwrap it

preprecessing ->

mention how you need to install home brew
|
brew update
brew install gcc open-mpi hdf4 hdf5 netcdf proj cdo nco
|
create a venv
python3 -m venv modis_env
source modis_env/bin/activate
|
pip install paackages to the venv
pip install --upgrade pip
pip install netCDF4 xarray numpy pandas pyhdf mpi4py

some cli tools arte needed before you canm pip install packages

<br>
cdo mergetime is used to combined all netcdf file into one. can be used for both modis or era5 data. when you download an era5 data it comes merged for each month, 
so for example if i used cdo mergetime 2m_temp_2022_01_rewrite.nc it will just give me the same output because all the days in january 2022 is already merged in one. cdo mergetime will be if im working on multiple months which is what i did on the project but you will end up with about 2gb so im just upload a sample so as viewers can understand


you "cdo mergetime" after "preprocessing_era" is done but before "era5_remapped"folder
