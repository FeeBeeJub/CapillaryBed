#! /usr/local/bin/python3

import threading
import pivotpi_servo
import pivotpi
import cyclic_barrier

if __name__ == '__main__':
    lgFlg=True
    numServos = 2
    ppi = pivotpi.PivotPi(addr = 0x40, actual_frequency = 60)
    ppilock = threading.Lock()
    stopThreadLock = threading.Lock()
    
    # By setting cbName in the Cyclic Barriers we enable logging for those barriers.
    # To disable, do not define cbName (You can also set it explicitly to None
    minPosCB = cyclic_barrier.CyclicBarrier(numServos, cbName="MinPosCB")
    maxPosCB = cyclic_barrier.CyclicBarrier(numServos, cbName="MaxPosCB")    
    
    servoNames = {}
    servoNames[0] = "Pulse_0"
    servoNames[1] = "Pulse_1"
    
    minPos = {}
    minPos[0] = 0
    minPos[1] = 0
    
    maxPos = {}
    maxPos[0] = 120
    maxPos[1] = 120
    
    pauseBeforeMin = {}
    pauseBeforeMin[0] = 0.5
    pauseBeforeMin[1] = 0.5
    
    pauseBeforeMax = {}
    pauseBeforeMax[0] = 0.2
    pauseBeforeMax[1] = 0.5
    
    ppst = {}
    
    for i in range(numServos):
        ppst[i] = pivotpi_servo.PivotPIServoThread(servoNames[i], ppi, ppilock, stopThreadLock, minPosCB, maxPosCB, i, minPos[i], maxPos[i], pauseBeforeMin[i], pauseBeforeMax[i], logFlag=lgFlg)
        ppst[i].start()
    np = eval( input("Input any integer to terminate:  ") )
    
    for i in range(numServos):
        ppst[i].stopServo()
    
    for i in range(numServos):
        ppst[i].join()
    
    print("DONE")
    
    