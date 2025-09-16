#!/bin/bash
# Earthdata Login Token EDL_TOKEN (replace with your actual token)
export $(grep -v '^#' .env | xargs)

# Output directory
outputdir="./MYD11A1_Africa"
# EDL_TOKEN="eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6ImRpcG9hZGVveWUiLCJleHAiOjE3NjMyNTExOTksImlhdCI6MTc1ODAzMzE5MywiaXNzIjoiaHR0cHM6Ly91cnMuZWFydGhkYXRhLm5hc2EuZ292IiwiaWRlbnRpdHlfcHJvdmlkZXIiOiJlZGxfb3BzIiwiYWNyIjoiZWRsIiwiYXNzdXJhbmNlX2xldmVsIjozfQ.aWS_nW61WsBEr7yuGMe2t5OYVNO_aivKVEFD49AHznIyJpo8hc0ESCQT7lzsqFECmvdJ73bAIrUtfOyEmexPm1wUl4I-vf6VAP9DKj7ry88_EWj4vez66fkSOXF-nYkQnAi1cCUykCmJ14GLe6rPx1QaHNLn9qS5UMlL2gPF_beiA5vubWq0THRzpbxSb4xyQ_XbxIKaqNwh_-pXBmQLZmXbhdwLra9xpapCatE21joKdOkulFH7tPSZPUMJ1retUK7fj2iybLyxO_zg8kazXMK5xFHpSbLGNQYvP9Bjn8fl182zN-IQsF1_f3b8OmMQBFiNODu4epqeHlBOBXwqOA"
mkdir -p "$outputdir"

# Product and collection
product=MYD11A1
collection=61

# Loop over years
for Year in {2001..2024}; do
    for Day in $(seq -f "%03g" 1 366); do
        # Build URL
        URL="https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/ ${collection}/${product}/${Year}/${Day}/"

        echo "Searching: $URL"

        # Download only files that contain 'h18v07' in the filename
        wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=5 \
            -A "*h18v07*.hdf","*h18v07*.hdf.xml" \
            "$URL" \
            --header="Authorization: Bearer $EDL_TOKEN" \
            -P "$outputdir"
    done
done

# goes into every folder 001,002 ..... 365 unwraps each folder and stores all the data a single folder from 2001001(01/01/2000) to 2024365(31/12/2024)
input_dir="./MYD11A1_Africa"
output_dir="./MYD11A1_Africa_final"

mkdir -p "$output_dir"  # Create output directory if it doesn't exist

for d in $(seq -w 1 365); do
    folder="$input_dir/$d"
    if [ -d "$folder" ]; then
#        # Move all files (not subfolders) from $folder to $output_dir
        cp "$folder"/* "$output_dir/"
    fi
done