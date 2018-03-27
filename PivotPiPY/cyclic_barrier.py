import threading
import sys
import logging
import pivotpi_logger

class BrokenBarrierException(Exception):
    def __init(self):
        Exception.__init__(self)
    
class CyclicBarrier(object):
    def __init__(self, numThreads, cbName=None):
        self._n = numThreads
        self._cnt = numThreads
        self._c = threading.Condition(threading.RLock())
        self._cbName=cbName
        self._lgr = None if not self._cbName else pivotpi_logger.PPILogger(logFileName="%s.log" % self._cbName, logLevel=logging.DEBUG)
        self._broken = False
    def doLogging(self, msg):
        if self._lgr:
            self._lgr.logDebugMessage("%s - %s: %s" % (self._cbName, threading.current_thread().name, msg))
    def await(self):
        with self._c:
            if self._broken:
                self.doLogging("Broken, notifying all and raising BrokenBarrierException")
                self._c.notify_all()
                raise BrokenBarrierException
            try:
                self._cnt -= 1
                if self._cnt:
                    self.doLogging("num waiting = %d" % (self._n - self._cnt))
                    self._c.wait()
                else:
                    self.doLogging("notifying all")
                    self._cnt = self._n
                    self._c.notify_all()
                self.doLogging("Leaving")
            except:
                print("Unexpected Exception of type %s in Thread %s - Breaking Barrier" % (sys.exc_info()[0], threading.current_thread().name))
                self.doLogging("Unexpected Exception of type %s - Breaking Barrier and notifying all" % sys.exc_info()[0])
                self._broken = True
                self._c.notify_all()
            finally:
                if self._broken:
                    self._c.notify_all()
                    raise BrokenBarrierException
    def breakAndFlush(self):
        with self._c:
            self._broken = True
            self._c.notify_all()
