from utils import read_modis, inverse_maps, Era_interpolation


input_folder="MOD11A1_Day_Terra_treated"
era5_file_path="skin_temp_rewritten_merged_remapped.nc"
output_folder = "interp_day_Terra"
view_time='Day'
Era_interpolation(input_folder, era5_file_path, output_folder,view_time=view_time)