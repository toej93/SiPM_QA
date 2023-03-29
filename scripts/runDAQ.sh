#!/bin/bash
###################################################################
#title			:runDAQ.sh
#description	:This script will start data acquisition for a given PCB_ID.
#author			:Jorge Torres
#date			:Mar 2023
#usage			:bash runDAQ.sh -i <PCB_ID> -n <Name of the person running this program>
###################################################################


display_usage() { 
	echo -e "\nUsage: $0 -i <PCB_ID> -n <Name of the person running this program> \n" 
	} 
# if less than two arguments supplied, display usage 
	if [  $# -le 2 ] 
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

echo Starting DAQ for PCB with ID: "$id_SiPM"

dataDir=/home/coure/SiPMs_QA/data
newDir="$dataDir/SiPM_$id_SiPM"
echo "Data will be saved in $newDir"
mkdir -p $newDir

configFile=/home/coure/SiPMs_QA/configFiles/muonVeto.cfg
outFileName=test.dat
outFile="$newDir/$outFileName"
echo $outFile
echo Starting wavedump now with the following config file: $configFile
wavedump $configFile $outFile
if [ $? -eq 0 ]; then
    echo Setup successful. Starting DAQ now
    exitReturn="successful"
else
    echo -e "\e[1;41mDAQ failed, aborting...\e[1;m"
    exitReturn="failed"
    exit 1
fi
dateEnd=$(date)
echo "Program was started at $dateStart by $name" > $newDir/log_$id_SiPM.txt
echo "And ended at $dateEnd with exit status: $exitReturn" >> $newDir/log_$id_SiPM.txt
