import unittest
import logging
import sys
import threading
import random
import time
import cyclic_barrier
import pivotpi_logger

class cyclicBarrierSlaveThread(threading.Thread):
    def __init__(self, pid, cyclicBarrier0, cyclicBarrier1, stopLock, logFlag=False, sleepTime=-1):
        super().__init__(name="CyclicBarrierSlave_%d" % int(pid))
        self._pid = int(pid)
        self._cb0 = cyclicBarrier0
        self._cb1 = cyclicBarrier1
        self._contFlag = True
        self._lFlag = logFlag
        self._lgr = None
        self._slp = float(sleepTime)
        self._sl = stopLock
    def stopThread(self):
        with self._sl:
            self.doLogging("Setting contFlag to False")
            self._contFlag = False
            self._cb0.breakAndFlush()
            self._cb1.breakAndFlush()
    def continueFlag(self):
        with self._sl:
            return self._contFlag
    def doLogging(self, msg):
        if self._lgr:
            self._lgr.logDebugMessage(msg)
    def initThread(self):
        self._lgr = None if not self._lFlag else pivotpi_logger.PPILogger(logFileName="%s.log" % self.name, logLevel=logging.DEBUG)
    def finalizeThread(self):
        self.doLogging("terminating")
        if self._lgr:
            self._lgr.finalizeLogger()
    def simulateWork(self, cbId):
        slpTm = 0.0
        if cbId == 1 and self._pid%2 == 0:
            slpTm = self._slp if (self._slp > 0.0) else 3.1*random.random()
        self.doLogging("cbId = %d, pid = %d, slpTm = %.2f" % (cbId, self._pid, slpTm))
        time.sleep(slpTm)
        self.doLogging("awaiting %d" % int(cbId))
    def run(self):
        self.initThread()
        try:
            while self.continueFlag():
                self._cb0.await()
                self.simulateWork(0)
                self._cb1.await()
                self.simulateWork(1)
        except cyclic_barrier.BrokenBarrierException:
            self.doLogging("BrokenBarrierException caught")
        except:
            self.doLogging("Unexpected error:  %s" % sys.exc_info()[0])
            print("Unexpected error:  %s" % sys.exc_info()[0])
        finally:
            self.finalizeThread()

class Test(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def testBrokenBarriers(self):
        nt = 20
        numTests = 20
        for i in range(numTests):
            errMsg = "All Threads Terminated Cleanly"
            threadsTerminatedCleanly = True
            print("Broken Barrier Test Iteration %d" % i)
            try:
                threadSet = set()
                cb0 = cyclic_barrier.CyclicBarrier(nt)
                cb1 = cyclic_barrier.CyclicBarrier(nt)
                sl = threading.Lock()
                for j in range(nt):
                    threadSet.add(cyclicBarrierSlaveThread(j, cb0, cb1, sl, logFlag=True))
                for thrd in threadSet:
                    thrd.start()
                time.sleep(7.7)
                for thrd in threadSet:
                    time.sleep(0.3*random.random())
                    thrd.stopThread()
                
                for thrd in threadSet:
                    thrd.join(10)
                    if thrd.is_alive() and threadsTerminatedCleanly:
                        errMsg = "Alive Thread Found: %s, Not All Threads Terminated Cleanly" % thrd.name
                        threadsTerminatedCleanly = False
                        break

                self.assertTrue(threadsTerminatedCleanly, errMsg)
                print("Test Broken Barriers Iteration %d Passed" % i)
            except AssertionError as assertError:
                raise assertError
            except:
                print("Unexpected error: %s - %s" % (sys.exc_info()[0], sys.exc_info()[1]))

if __name__ == "__main__":
    #sys.argv = ['', 'Test.testName']
    unittest.main()