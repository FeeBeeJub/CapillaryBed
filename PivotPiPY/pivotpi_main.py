#! /usr/local/bin/python3

'''
Created on Mar 22, 2018

@author: rob
'''
import threading
import pivotpi_servo
import pivotpi

if __name__ == '__main__':
    servoName = "Pulse_0"
    ppi = pivotpi.PivotPi(addr = 0x40, actual_frequency = 60)
    ppilock = threading.Lock()
    channel = 0
    minPos = 20
    maxPos = 160
    pauseAtMin = 1
    pauseAtMax = 2
    ppst = pivotpi_servo.PivotPIServoThread(servoName, ppi, ppilock, channel, minPos, maxPos, pauseAtMin, pauseAtMax)
    
    ppst.start()
    
    np = eval( input("Input any integer to terminate:  ") )
    
    ppst.stopServo()
    
    print("DONE")