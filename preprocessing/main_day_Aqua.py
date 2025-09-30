from utils import read_modis, inverse_maps, LST_extraction
input_folder="./MYD11A1_Africa_final"
var="LST_Day_1km"
qc_var="QC_Day"
varo="lst_day"
output_folder="./MYD11A1_Day_Aqua_treated"
LST_extraction(input_folder, var, qc_var, varo, output_folder)