#!/bin/bash
###################################################################
#title			:runDAQ_gainV.sh
#description	:This script will start data acquisition for a given PCB_ID, and run
                #for different voltages
#author			:Jorge Torres
#date			:May 2023
#usage			:bash runDAQ_gainV.sh -i <PCB_ID> -n <Name of the person running this program>
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

echo "Set the HV power supply to 55.0 V, and the 'frequency' lever in the LED to 'high'. Write 'done' and then press enter"
read input_1

# echo Starting DAQ for PCB with ID: "$id_SiPM"

dataDir=/home/coure/SiPMs_QA/data
newDir="$dataDir/SiPM_$id_SiPM"
# if [ -d "$newDir" ]; then
#     echo -e "\e[1;41m$newDir already exists, pick another ID...\e[1;m"
#     exit 1
# fi
echo "Data will be saved in $newDir"
# mkdir -p $newDir

configFile=/home/coure/SiPMs_QA/configFiles/muonVeto_fast.cfg
for V_bias in $(seq 55 0.5 59) #Loop over different bias voltages
do
    echo "Set the HV power supply to $V_bias. Write 'done' and then press enter"
    read input_2

    outFileName=SiPM_$id_SiPM_$V_bias.dat
    outFile="$newDir/$outFileName"
    echo $outFile
    echo Starting wavedump now with the following config file: $configFile
    wavedump $configFile $outFile
    # wait
    if [ $? -eq 0 ]; then
        # echo Setup successful. Starting DAQ now
        exitReturn="successful"
    else
        echo -e "\e[1;41mDAQ failed, aborting...\e[1;m"
        exitReturn="failed"
        dateEnd=$(date)
        echo "Looping over voltage bias was started at $dateStart by $name" >> $newDir/log_$id_SiPM.txt
        echo "And ended at $dateEnd at bias V $V_bias with exit status: $exitReturn" >> $newDir/log_$id_SiPM.txt

        exit 1
    fi
done

dateEnd=$(date)
echo "Looping over voltage bias was started at $dateStart by $name" >> $newDir/log_$id_SiPM.txt
echo "And ended at $dateEnd at bias V $V_bias with exit status: $exitReturn" >> $newDir/log_$id_SiPM.txt

echo "Return the 'frequency' lever in the LED to 'low'. Write 'done' and then press enter"
read input_3

echo "Done taking data!"