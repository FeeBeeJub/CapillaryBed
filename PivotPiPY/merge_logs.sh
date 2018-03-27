#! /bin/bash

logfilesToMerge=(MaxPosCB.log
				 MinPosCB.log
				 MockPivotPi.log
				 Pulse_0.log
				 Pulse_1.log
				 Pulse_2.log
				 Pulse_3.log
				 Pulse_4.log
				 Pulse_5.log
				 Pulse_6.log
				 Pulse_7.log
				 )

if [ -d logs ] ; then
	if [ -e logs/mergedLogs.txt ] ; then
		rm -f logs/mergedLogs.txt
	fi
	
	if [ -e logs/mergedLogs.txt.tmp ] ; then
		rm -f logs/mergedLogs.txt.tmp
	fi
	
	for fname in ${logfilesToMerge[*]}
	do
		if [ -e logs/${fname} ] ; then
			cat logs/${fname} >> logs/mergedLogs.txt.tmp
		fi
	done
	
	if [ -e logs/mergedLogs.txt.tmp ] ; then
		cat logs/mergedLogs.txt.tmp | sort > logs/mergedLogs.txt
		rm -f logs/mergedLogs.txt.tmp
	fi
else
	echo "logs directory does not exist"
fi

