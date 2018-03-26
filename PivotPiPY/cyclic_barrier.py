import threading

class CyclicBarrier(object):
    def __init__(self, numThreads, cbName=None):
        self._n = numThreads
        self._cnt = numThreads
        self._c = threading.Condition(threading.Lock())
        self._cbName=cbName
    def await(self):
        self._c.acquire()
        self._cnt -= 1
        if self._cnt:
            if self._cbName:
                print("%s %s: num waiting = %d" % (self._cbName, threading.current_thread().name, self._n - self._cnt))
            self._c.wait()
        else:
            if self._cbName:
                print("%s %s: notifying all" % (self._cbName, threading.current_thread().name))
            self._cnt = self._n
            self._c.notify_all()
        if self._cbName:
            print("%s %s: Leaving" % (self._cbName, threading.current_thread().name))
        self._c.release()
    def flush(self):
        self._c.acquire()
        self._c.notify_all()
        self._c.release()
    