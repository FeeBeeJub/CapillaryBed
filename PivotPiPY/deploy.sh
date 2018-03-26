#! /bin/bash

targetMachines=(pulse000)
deployFiles=(pivotpi_logger.py
             pivotpi_main.py
             cyclic_barrier.py
             pivotpi_servo.py)

SOURCE_PATH=${HOME}/git/Pivot-Pi-Simple/PivotPiPY
TARGET_PATH=/home/pi/PivotPi

SOURCE_PYTHON_INTERPRETER=/usr/local/bin/python3
TARGET_PYTHON_INTERPRETER=/usr/bin/python3

for targetMach in "${targetMachines[@]}" ; do
	echo "Creating Deploy Directory on ${targetMach} (ignore errors if already exists)"
	ssh ${targetMach} "mkdir ${TARGET_PATH}"
	for fileName in "${deployFiles[@]}" ; do
		echo "Deploying ${SOURCE_PATH}/${fileName} to ${targetMach}:${TARGET_PATH}/${fileName}"
		scp -p ${SOURCE_PATH}/${fileName} pi@${targetMach}:${TARGET_PATH}/${fileName}.tmp
		
		ssh ${targetMach} "sed 's:${SOURCE_PYTHON_INTERPRETER}:${TARGET_PYTHON_INTERPRETER}:' < ${TARGET_PATH}/${fileName}.tmp > ${TARGET_PATH}/${fileName}"
		
		ssh ${targetMach} "rm -f ${TARGET_PATH}/${fileName}.tmp"
		
		echo "ssh ${targetMach} 'chmod a+x ${TARGET_PATH}/${fileName}'"
		ssh ${targetMach} "chmod a+x ${TARGET_PATH}/${fileName}"
	done
done
