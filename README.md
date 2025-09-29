download_modis -> download the modis(MOD11A1 and MYD11A1) data
download_era5 -> downloads era5 2m temperature and skin temperatur

# include image of how is looks ehen download 001 002
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


## Repository Structure

├── download_era5/                # Scripts and data for downloading ERA5 datasets
│   ├── 2m_temp_2022_2024_africa/ # Where Era5 2m temperature data is stored
│   ├── skin_temp_2022_2004_africa/ # Where Era5 Skin temperature data is stored
│   ├── download_era5_2mtemp/     # Scripts for 2m temperature download
│   └── download_era5_skintemp/   # Scripts for skin temperature download
│
├── download_modis/               # Scripts for downloading MODIS LST products
│   ├── download_mod11a1_africa.sh
│   └── download_myd11a1_africa.sh
│
├── era5_modis_interpolation/     # Python scripts for interpolating ERA5 to MODIS grid (the prepares it for training)
│
├── era5_remapped/                # ERA5 remapping configurations
│
├── preprocessing/                # Preprocessing Modis data(QA assessment, saving if the image was taken to a different(day or night) and saving it to netcdf)
│
├── preprocessing_era5/           # Preprocessing Era5 data(rewrite to netcdf and then merge into a single netcdf file)


# Clone the repo

git clone https://github.com/JordanAdeoye/MODIS-LST-Reconstruction.git
cd MODIS-LST-Reconstruction

# Install Dependencies

# If running locally(would not suggest)/EC2

sudo apt-get update
sudo apt-get install -y gcc gfortran libopenmpi-dev openmpi-bin libhdf4-dev libhdf5-dev libnetcdf-dev proj-bin cdo
pip install -r requirements.txt

# If running on AllianceCan HPC(As i did) 
module load python/3.11.5
module load hdf/4.2.16
module load gcc/12.3
module load openmpi/4.1.5
module load hdf5
module load netcdf
module load mpi4py
module load proj/9.4.1
module load cdo/2.2.2

pip install -r requirements.txt

# Workflow

1. Download Modis data

   i used two modis products MOD11A1 and MYD11A1 which are on bothe two sattelite Terra and Aqua repectively
   
before running
   bash download_modis/download_mod11a1_africa.sh
    bash download_modis/download_myd11a1_africa.sh
    
   you need to have a .netrc file in your home directory containing your nasa earth login and password
   
machine urs.earthdata.nasa.gov
login your_username
password your_password

the results from the downloads are usually in the forms
<img width="1368" height="205" alt="001 to 366" src="https://github.com/user-attachments/assets/86042696-d78c-44ff-845c-3899e87df0a0" />

then we unpack it and store in download_modis/MOD11A1_Africa_final and download_modis/MYD11A1_Africa_final

2. preprocessing Modis data


   













MODIS = Moderate Resolution Imaging Spectroradiometer, an instrument onboard NASA’s satellites.

It flies on two satellites:

Terra (morning overpass) → products start with MOD (e.g., MOD11A1)

Aqua (afternoon overpass) → products start with MYD (e.g., MYD11A1)

11A1 = the specific product for daily Land Surface Temperature (LST) and emissivity at 1 km resolution.
