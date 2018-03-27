import time
import sys
import threading
import pivotpi_logger
import cyclic_barrier

class PivotPIServoThread(threading.Thread):
    '''Servo Thread for Pivot Pi.'''

    def __init__(self, servoName, ppi, ppilock, stopLock, minPosCB, maxPosCB, channel, minPos, maxPos, pauseBeforeMin, pauseBeforeMax, logFlag=False):
        '''
        Construct a PivotPIServoThread
        
        Keyword arguments:
        servoName -- The Name of the Servo (will be used as name of log file)
        ppi -- The Pivot Pi
        ppilock -- An instance of a threading.Lock(), used to insure thread-safe access to Pivot PI
        channel -- The channel of the servo (0 - 7)
        minPos -- The minimum angle of the servo, between 0 and maxPos
        maxPos -- The maximum angle of the servo, between minPos and 180
        pauseBeforeMin -- The length of time (in seconds) to dwell before servo is set to minimum angle
        pauseBeforeMax -- The length of time (in seconds) to dwell before servo is set to maximum angle
        '''
        super().__init__(name=servoName)
        if not PivotPIServoThread.validateParams(channel, minPos, maxPos, pauseBeforeMin, pauseBeforeMax):
            raise ValueError("Invalid Parameters for Servo = %s" % servoName)
        self._ppi = ppi
        self._ppilock = ppilock
        self._sl = stopLock
        self._minPosCB = minPosCB
        self._maxPosCB = maxPosCB
        self._c = int(channel)
        self._minP = int(minPos)
        self._maxP = int(maxPos)
        self._pbMin = max(0.0, float(pauseBeforeMin))
        self._pbMax = max(0.0, float(pauseBeforeMax))
        self._continue = True
        self._logFlag = logFlag
        self._lgr = None
        self._paramLock = threading.Lock()
    @staticmethod
    def validateParams(channel, minPos, maxPos, pauseBeforeMin, pauseBeforeMax):
        ret = True
        if int(channel) < 0 or int(channel) > 7:
            print("Invalid Channel:  %d" % channel)
            ret = False
        if int(minPos) < 0 or int(maxPos) > 180 or int(minPos) > int(maxPos):
            print("Invalid minPos = %d and/or maxPos = %d" % (minPos, maxPos))
            ret = False
        if float(pauseBeforeMin) < 0.0 or float(pauseBeforeMax) < 0.0:
            print("Invalid pauseBeforeMin = %.2f and/or pauseBeforeMax = %.2f" % (pauseBeforeMin, pauseBeforeMax))
            ret = False
        return ret
    def initThread(self):
        self._lgr = None if not self._logFlag else pivotpi_logger.PPILogger("%s.log" % self.name)
    def finalizeThread(self):
        self.doLogging("Finalizing")
        self._minPos(self.getPositionsAndPauses())
        if self._logFlag:
            self._lgr.finalizeLogger()
    def doLogging(self, msg):
        if self._logFlag:
            self._lgr.logDebugMessage(msg)
    def stopServo(self):
        with self._sl:
            self._continue = False
            self._minPosCB.breakAndFlush()
            self._maxPosCB.breakAndFlush()
    def continueFlag(self):
        with self._sl:
            return self._continue
    def _minPos(self, papMap):
        with self._ppilock:
            self._ppi.led(papMap['channel'], 0)
            self._ppi.angle(papMap['channel'], papMap['min'])
        self.doLogging("MIN:  %d     Channel:  %d" % (papMap['min'], papMap['channel']))
    def _maxPos(self, papMap):
        with self._ppilock:
            self._ppi.led(papMap['channel'], 100)
            self._ppi.angle(papMap['channel'], papMap['max'])
        self.doLogging("MAX:  %d     Channel:  %d" % (papMap['max'], papMap['channel']))
    def minPos(self):
        papMap = self.getPositionsAndPauses()
        time.sleep(papMap['pauseBeforeMin'])
        self._minPos(papMap)
        time.sleep(0.1)
    def maxPos(self):
        papMap = self.getPositionsAndPauses()
        time.sleep(papMap['pauseBeforeMax'])
        self._maxPos(papMap)
        time.sleep(0.1)
    def setPositionsAndPauses(self, channel, minPos, maxPos, pauseBeforeMin, pauseBeforeMax):
        if not PivotPIServoThread.validateParams(channel, minPos, maxPos, pauseBeforeMin, pauseBeforeMax):
            print("Invalid Parameters")
        else:
            with self._paramLock:
                self._c = int(channel)
                self._minP = int(minPos)
                self._maxP = int(maxPos)
                self._pbMin = max(0.0, float(pauseBeforeMin))
                self._pbMax = max(0.0, float(pauseBeforeMax))
    def getPositionsAndPauses(self):
        ret = {}
        with self._paramLock:
            ret['channel'] = self._c
            ret['min'] = self._minP
            ret['max'] = self._maxP
            ret['pauseBeforeMin'] = self._pbMin
            ret['pauseBeforeMax'] = self._pbMax
        return ret
    def run(self):
        self.initThread()
        try:
            while self.continueFlag():
                self._minPosCB.await()
                self.minPos()
                self._maxPosCB.await()
                self.maxPos()
        except cyclic_barrier.BrokenBarrierException:
            self.doLogging("Broken Barrier Exception Caught, this is OK") # This is OK, we expect the barrier to be broken at end of thread execution
        except:
            self.doLogging("Unexpected error:  %s" % sys.exc_info()[0])
            print("Unexpected error:  %s" % sys.exc_info()[0])
        finally:
            self.finalizeThread()
        