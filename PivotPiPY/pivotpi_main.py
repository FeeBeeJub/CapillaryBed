#! /usr/local/bin/python3

'''
Created on Mar 22, 2018

@author: rob
'''
import threading
import pivotpi_servo
import pivotpi


if __name__ == '__main__':
    servoNames = {}
    servoNames[0] = "Pulse_0"
    servoNames[1] = "Pulse_1"
    minPos = {}
    minPos[0] = 0
    minPos[1] = 0
    maxPos = {}
    maxPos[0] = 120
    maxPos[2] = 120
    
    ppi = pivotpi.PivotPi(addr = 0x40, actual_frequency = 60)
    ppilock = threading.Lock()
    channel = 0
    pauseAtMin = {}
    pauseAtMin[0] = 0.5
    pauseAtMin[1] = 0.5
    pauseAtMax = {}
    pauseAtMax[0] = 0.5
    pauseAtMax[1] = 0.5
    
    ppst = {}
    
    for i in range(2):
        ppst[i] = pivotpi_servo.PivotPIServoThread(servoNames[i], ppi, ppilock, i, minPos[i], maxPos[i], pauseAtMin[i], pauseAtMax[i])
        ppst[i].start()
    np = eval( input("Input any integer to terminate:  ") )
    
    for i in range(2):
        ppst[i].stopServo()
    
    for i in range(2):
        ppst[i].join()
    
    print("DONE")
    
    