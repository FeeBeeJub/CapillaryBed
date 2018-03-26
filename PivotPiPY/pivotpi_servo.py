import time
import threading
import pivotpi_logger

class PivotPIServoThread(threading.Thread):
    '''Servo Thread for Pivot Pi.'''

    def __init__(self, servoName, ppi, ppilock, cyclicBarrier, channel, minPos, maxPos, pauseAtMin, pauseAtMax):
        '''
        Construct a PivotPIServoThread
        
        Keyword arguments:
        servoName -- The Name of the Servo (will be used as name of log file)
        ppi -- The Pivot Pi
        ppilock -- An instance of a threading.Lock(), used to insure thread-safe access to Pivot PI
        channel -- The channel of the servo (0 - 7)
        minPos -- The minimum angle of the servo, between 0 and maxPos
        maxPos -- The maximum angle of the servo, between minPos and 180
        pauseAtMin -- The length of time (in seconds) to dwell at the minimum angle
        pauseAtMax -- The length of time (in seconds) to dwell at the maximum angle
        '''
        super().__init__(name=servoName)
        if not PivotPIServoThread.validateParams(channel, minPos, maxPos, pauseAtMin, pauseAtMax):
            raise ValueError("Invalid Parameters for Servo = %s" % servoName)
        self._nm = servoName
        self._ppi = ppi
        self._ppilock = ppilock
        self._cb = cyclicBarrier
        self._c = int(channel)
        self._minP = int(minPos)
        self._maxP = int(maxPos)
        self._paMin = max(0.0, float(pauseAtMin))
        self._paMax = max(0.0, float(pauseAtMax))
        self._continue = True
        self._lgr = pivotpi_logger.PPILogger("%s.log" % servoName)
        self._paramLock = threading.Lock()
    @staticmethod
    def validateParams(channel, minPos, maxPos, pauseAtMin, pauseAtMax):
        ret = True
        if int(channel) < 0 or int(channel) > 7:
            print("Invalid Channel:  %d" % channel)
            ret = False
        if int(minPos) < 0 or int(maxPos) > 180 or int(minPos) > int(maxPos):
            print("Invalid minPos = %d and/or maxPos = %d" % (minPos, maxPos))
            ret = False
        if float(pauseAtMin) < 0.0 or float(pauseAtMax) < 0.0:
            print("Invalid pauseAtMin = %.2f and/or pauseAtMax = %.2f" % (pauseAtMin, pauseAtMax))
            ret = False
        return ret
    def stopServo(self):
        self._continue = False
    def minPos(self):
        papMap = self.getPositionsAndPauses()
        self._ppilock.acquire()
        self._ppi.led(papMap['channel'], 0)
        self._ppi.angle(papMap['channel'], papMap['min'])
        self._lgr.logDebugMessage("MIN:  %d     Channel:  %d" % (papMap['min'], papMap['channel']))
        time.sleep(papMap['pauseAtMin'])
        self._ppilock.release()
    def maxPos(self):
        papMap = self.getPositionsAndPauses()
        self._ppilock.acquire()
        self._ppi.led(papMap['channel'], 100)
        self._ppi.angle(papMap['channel'], papMap['max'])
        self._lgr.logDebugMessage("MAX:  %d     Channel:  %d" % (papMap['max'], papMap['channel']))
        time.sleep(papMap['pauseAtMax'])
        self._ppilock.release()
    def setPositionsAndPauses(self, channel, minPos, maxPos, pauseAtMin, pauseAtMax):
        if not PivotPIServoThread.validateParams(channel, minPos, maxPos, pauseAtMin, pauseAtMax):
            print("Invalid Parameters")
        else:
            self._paramLock.acquire()
            self._c = int(channel)
            self._minP = int(minPos)
            self._maxP = int(maxPos)
            self._paMin = max(0.0, float(pauseAtMin))
            self._paMax = max(0.0, float(pauseAtMax))
            self._paramLock.release()
    def getPositionsAndPauses(self):
        ret = {}
        self._paramLock.acquire()
        ret['channel'] = self._c
        ret['min'] = self._minP
        ret['max'] = self._maxP
        ret['pauseAtMin'] = self._paMin
        ret['pauseAtMax'] = self._paMax
        self._paramLock.release()
        return ret
    def run(self):
        while self._continue:
            self.minPos()
            self.maxPos()
        