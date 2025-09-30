from rewrite import rewrite_func

input_dir="./download_era5/2m_temp_2022_2024_africa"
output_dir="./2m_temperature_rewriten"
temp_long_name = "2 metre temperature"
var_name = "t2m"

rewrite_func(input_dir,output_dir,var_name,temp_long_name)