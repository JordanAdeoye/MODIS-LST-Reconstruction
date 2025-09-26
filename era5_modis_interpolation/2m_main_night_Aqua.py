from utils_2m import read_modis, inverse_maps, Era_interpolation

input_folder="MYD11A1_Night_Aqua_treated"
era5_file_path="2m_temp_rewritten_merged_remapped.nc"
output_folder = "2m_interp_night_Aqua"
view_time='Night'
Era_interpolation(input_folder, era5_file_path, output_folder,view_time=view_time)