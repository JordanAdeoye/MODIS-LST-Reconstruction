from utils import read_modis, inverse_maps, LST_extraction
input_folder="./MOD11A1_Africa_final"
var="LST_Night_1km"
qc_var="QC_Night"
varo="lst_night"
output_folder="./MOD11A1_Night_Terra_treated"
LST_extraction(input_folder, var, qc_var, varo, output_folder)