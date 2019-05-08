#!/bin/bash

if [ "$1" = "" ]; then
	echo "This script creates EMEP-friendly links to WRF output files."
    echo "usage (in directory where you want the links to appear): "
    echo "                link_met_data_script.sh [path_to_WRF_data_directory]"
    exit
fi


file_list=$(ls -1 $1/wrfout*)

for FILE in ${file_list[@]};
do
	parts=(${FILE//// })  # this splits FILE string on the / delimiter

	filename=${parts[${#parts[@]}-1]}

	fileparts=(${filename//:/ })
	
	LOCAL_FILE=${fileparts[0]}

	ln -s $FILE $LOCAL_FILE  

done