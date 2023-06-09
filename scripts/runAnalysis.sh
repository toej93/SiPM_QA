#!/bin/bash
###################################################################
#title			:runDAQ.sh
#description    :This script will start data acquisition for a given PCB_ID.
#author			:Jorge Torres
#date			:Mar 2023
#usage			:bash runDAQ.sh -i <PCB_ID> -n
###################################################################


display_usage() { 
	echo -e "\nUsage: $0 -i <PCB_ID> \n" 
	} 
# if less than two arguments supplied, display usage 
	if [  $# -le 1 ] 
	then 
		display_usage
		exit 1
	fi 

# This program will start the data acquisition and control the data output

while getopts i:n:c: flag
do
    case "${flag}" in
        i) id_SiPM="${OPTARG}";;
        n) name=${OPTARG};;
		c) channel="${OPTARG}";;
    esac
done
dateStart=$(date)

echo Starting analysis for PCB with ID: "$id_SiPM"

dataDir=/home/coure/SiPMs_QA/results
newDir="$dataDir/SiPM_$id_SiPM-$(date +"%d-%m-%Y")/"
mkdir -p $newDir
echo "Results will be saved in $newDir"
if python runAnalysis.py $id_SiPM $newDir $channel; then
    echo "Analysis code ran successfully. Plots saved in $newDir"
else
    echo "Analysis code failed"
fi

# dateEnd=$(date)
# echo "Program was started at $dateStart" > $newDir/log_$id_SiPM.txt
# echo "And ended at $dateEnd with " >> $newDir/log_$id_SiPM.txt
