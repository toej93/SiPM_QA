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

while getopts i:n: flag
do
    case "${flag}" in
        i) id_SiPM="${OPTARG}";;
        n) name=${OPTARG};;
    esac
done
dateStart=$(date)

echo Starting analysis for PCB with ID: "$id_SiPM"

dataDir=/home/coure/SiPMs_QA/results
newDir="$dataDir/SiPM_$id_SiPM/"
mkdir $newDir
echo "Results will be saved in $newDir"

python runAnalysis.py $id_SiPM

# configFile=/home/coure/SiPMs_QA/configFiles/test.cfg
# outFileName=test.dat
# outFile="$newDir/$outFileName"
# echo $outFile
# echo Starting wavedump now with the following config file: $configFile
# wavedump $configFile $outFile
# if [ $? -eq 0 ]; then
#     echo Setup successful. Starting DAQ now
# else
#     echo -e "\e[1;41mDAQ failed, aborting...\e[1;m"
#     exit 1
# fi
# dateEnd=$(date)
# echo "Program was started at $dateStart" > $newDir/log_$id_SiPM.txt
# echo "And ended at $dateEnd with " >> $newDir/log_$id_SiPM.txt
