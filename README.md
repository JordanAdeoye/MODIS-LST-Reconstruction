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
