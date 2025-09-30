

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

**Note:** This repository includes sample data for January 2022 only. The full project uses data from January 2022 to December 2024.

## 1. Download MODIS Data

This project uses two MODIS products:
- **MOD11A1** - Terra satellite
- **MYD11A1** - Aqua satellite

### Prerequisites

Before running the download scripts, you need to create a `.netrc` file in your home directory with your NASA Earthdata login credentials:

machine urs.earthdata.nasa.gov
login your_username
password your_password

### Running the Download Scripts
```bash
bash download_modis/download_mod11a1_africa.sh
bash download_modis/download_myd11a1_africa.sh
```

### Output

The downloaded files are organized by day of year (001 to 366):

<img width="1368" height="205" alt="001 to 366" src="https://github.com/user-attachments/assets/86042696-d78c-44ff-845c-3899e87df0a0" />

The data is then unpacked and stored in:
* `download_modis/MOD11A1_Africa_final/`
* `download_modis/MYD11A1_Africa_final/`


2. ## Preprocessing MODIS Data

   ### Overview
   `preprocessing/utils.py` contains functions to:
   - Read MODIS HDF files
   - Convert MODIS sinusoidal projection to geographic coordinates
   - Extract LST products from HDF files
   - Apply Quality Assurance (QA) filtering using QC flags
   - Save processed data as NetCDF files

   ### Quality Control
   QC flags are decoded to filter pixels based on:
   - Mandatory quality flag (accept 0 or 1)
   - Data quality flag (accept 0 or 1)  
   - Emissivity error flag (accept 0 only)
   - LST error flag (accept 0 only)

   Pixels failing any criteria are masked as NaN.

   ### Usage
   Run preprocessing for each satellite and observation time:
   ```bash
   python3 preprocessing/main_day_Aqua.py
   python3 preprocessing/main_night_Aqua.py
   python3 preprocessing/main_day_Terra.py
   python3 preprocessing/main_night_Terra.py
   ```
  ### Output:

* `preprocessing/MYD11A1_Day_Aqua_treated/`
* `preprocessing/MYD11A1_Night_Aqua_treated/`
* `preprocessing/MOD11A1_Day_Terra_treated/`
* `preprocessing/MOD11A1_Night_Terra_treated/`


## 3. Download ERA5 Data

Downloads 2-meter temperature and skin temperature data.

### To Run:
```bash
python3 download_era5/download_era5_2mtemp.py
python3 download_era5/download_era5_skintemp.py
```
 ### Output:

* `download_era5/2m_temp_2022_2024_africa/`
* `download_era5/skin_temp_2022_2024_africa/`

## 4. Preprocessing ERA5 Data

`preprocessing_era5/rewrite.py` contains the function to rewrite the ERA5 data to NetCDF format.

### To Run:
```bash
python preprocessing_era5/rewrite_era5_2m_temp.py
python preprocessing_era5/rewrite_era5_skin_temp.py
```

### Output:

* `preprocessing_era5/2m_temperature_rewriten/`
* `preprocessing_era5/skin_temperature_rewriten/`

### Merging Data

`preprocessing_era5/mergetime_command.txt` contains the CDO commands to merge all the data for skin temperature and 2-meter temperature into single NetCDF files.

### Merged Output:

* `preprocessing_era5/skin_temperature_rewriten_merged.nc`
* `preprocessing_era5/2m_temperature_rewriten_merged.nc`


## 5. Remapping ERA5 Data to MODIS Grid (Spatial Interpolation)

This step spatially interpolates ERA5 data to match the MODIS grid resolution using bilinear interpolation.

### Grid Specification

`era5_remapped/grid_h18_v07.txt` defines the grid specification used to remap ERA5 data to match the MODIS grid resolution.

### To Run:

`era5_remapped/remap_command.txt` contains the CDO commands to perform bilinear interpolation of the ERA5 data to the MODIS grid.

### Output:

* `era5_remapped/2m_temperature_remapped.nc`
* `era5_remapped/skin_temperature_remapped.nc`



## 6. Interpolating ERA5 with MODIS

This process combines ERA5 temperature data with MODIS satellite observations. We have two types of temperature data:

### Core Processing Files:
- `era5_modis_interpolation/utils.py` → Interpolates ERA5 skin temperature with MODIS data
- `era5_modis_interpolation/utils_2m.py` → Interpolates ERA5 2-meter temperature with MODIS data

### Why separate files?
The data varies by time of day (day vs. night) and satellite (Aqua vs. Terra), requiring different processing scripts for each combination.

### To Run:

Execute the following scripts based on your data type and requirements:

**For 2-meter temperature:**
```bash
python era5_modis_interpolation/2m_main_day_Aqua.py      # Daytime, Aqua satellite
python era5_modis_interpolation/2m_main_day_Terra.py     # Daytime, Terra satellite
python era5_modis_interpolation/2m_main_night_Aqua.py    # Nighttime, Aqua satellite
python era5_modis_interpolation/2m_main_night_Terra.py   # Nighttime, Terra satellite
```
**For skin temperature:**
```bash
python era5_modis_interpolation/main_day_Aqua.py         # Daytime, Aqua satellite
python era5_modis_interpolation/main_day_Terra.py        # Daytime, Terra satellite
python era5_modis_interpolation/main_night_Aqua.py       # Nighttime, Aqua satellite
python era5_modis_interpolation/main_night_Terra.py      # Nighttime, Terra satellite
```   
### Output:

**For interpolated skin temperature:**
* `era5_modis_interpolation/interp_day_Aqua/`
* `era5_modis_interpolation/interp_night_Aqua/`
* `era5_modis_interpolation/interp_day_Terra/`
* `era5_modis_interpolation/interp_night_Terra/`

**For interpolated 2-meter temperature:**
* `era5_modis_interpolation/2m_interp_day_Aqua/`
* `era5_modis_interpolation/2m_interp_day_Terra/`
* `era5_modis_interpolation/2m_interp_night_Aqua/`
* `era5_modis_interpolation/2m_interp_night_Terra/`
   

   
   


   














