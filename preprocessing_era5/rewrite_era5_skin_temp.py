from rewrite import rewrite_func

input_dir="./download_era5/skin_temp_2022_2004_africa"
output_dir="./skin_temperature_rewriten"
temp_long_name = "Skin temperature"
var_name = "skt"

rewrite_func(input_dir,output_dir,var_name,temp_long_name)