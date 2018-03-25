'''
Created on Mar 22, 2018

@author: rob
'''

import os
import logging
import threading

createDirLock = threading.Lock()

class PPILogger(object):
    '''
    File Logger for PivotPi, Thread Safe.
    
    Writes log entries to logs/ directory under current directory, format is date/time followed by message.
    '''
    def __init__(self, logFileName, logLevel=logging.DEBUG):
        '''
        Construct a PivotPi Logger, create a logs/ directory in current directory if it does not already exist.
        
        Keyword arguments:
        logFileName -- The name of the log file
        logLevel -- The logging level (default logging.DEBUG)
        '''
        self._logFileName = logFileName
        self._logDirectory = self.createLogsDirIfNotExists()
        self._logFileAbsolutePath = "%s%s%s" % (self._logDirectory, os.sep, self._logFileName)
        self._logLevel = logLevel
        self._logger = self.getFileLogger()
    @staticmethod
    def createLogsDirIfNotExists():
        '''Create a logs/ directory if it does not already exist.'''
        createDirLock.acquire()
        ret = "%s%slogs" % (os.path.dirname(os.path.realpath(__file__)), os.sep)
        if not os.path.exists(ret):
            os.makedirs(ret)
        createDirLock.release()
        return ret
    def getFileLogger(self):
        '''Gets a logger for current thread.'''
        ret = logging.getLogger("%s_%s" % (__name__, threading.current_thread().name))
        ret.setLevel(self._logLevel)
        lgrFH = logging.FileHandler(self.logFileAbsolutePath())
        lgrFH.setLevel(self._logLevel)
        lgrFmtr = logging.Formatter('%(asctime)s - %(message)s')
        lgrFH.setFormatter(lgrFmtr)
        ret.addHandler(lgrFH)
        return ret
    def logDebugMessage(self, msg):
        '''Write Debug Message.'''
        self._logger.debug("%s:  %s" % (threading.current_thread().name, msg))
    def logInfoMessage(self, msg):
        '''Write Info Message.'''
        self._logger.info("%s:  %s" % (threading.current_thread().name, msg))
    def logWarningMessage(self, msg):
        '''Write Warning Message.'''
        self._logger.warning("%s:  %s" % (threading.current_thread().name, msg))
    def logErrorMessage(self, msg):
        '''Write Error Message.'''
        self._logger.error("%s:  %s" % (threading.current_thread().name, msg))
    def logCriticalMessage(self, msg):
        '''Write Critical Message.'''
        self._logger.critical("%s:  %s" % (threading.current_thread().name, msg))
    def logFileAbsolutePath(self):
        '''Return absolute path to log file.'''
        return self._logFileAbsolutePath