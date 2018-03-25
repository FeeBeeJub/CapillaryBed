'''
Created on Mar 22, 2018

@author: rob
'''

import logging
import pivotpi_logger

# DO NOT COPY THIS FILE TO THE TARGET RASPBERRY PI.
# THIS IS ONLY FOR TESTING ON THE DEVELOPMENT MACHINE.
# IN AN ACTUAL ENVIRONMENT YOU SHOULD PICK UP DexterLab's
# pivotpi.py FILE AND USE THE ACTUAL PivotPi CLASS.

class PivotPi(object):
    '''Dummy PivotPi package for simulation - DO NOT COPY TO RaspberryPi'''
    def __init__(self, addr = 0x40, actual_frequency = 60):
        self._lgr = pivotpi_logger.PPILogger(logFileName="MockPivotPi.log", logLevel=logging.DEBUG)
        del addr  # Indicate that addr is unused
        del actual_frequency  # Indicate that actual_frequency is unused.
    def pwm(self, channel, on, off):
        self._lgr.logDebugMessage("PivotPi.pwm(channel = %d, on = %d, off = %d" % (channel, on, off))
    def angle(self, channel, servoPosn):
        try:  
            if servoPosn >= 0 and servoPosn <= 180 and channel >= 0 and channel <= 7:
                self._lgr.logDebugMessage("PivotPi.servoPosn(channel = %d, servoPosn = %d)" % (channel, servoPosn))
            else:
                self._lgr.logDebugMessage("PivotPi.servoPosn - INVALID ARGUMENTS: channel = %d, servoPosn = %d" % (channel, servoPosn))
        except TypeError as tErr:
            print("TypeError: {0}".format(tErr))
    def led(self, channel, percent):
        if channel >= 0 and channel <= 7:
            self._lgr.logDebugMessage("PivotPi.led(channel = %d, percent = %.2lf)" % (channel, percent))
        else:
            self._lgr.logDebugMessage("PivotPi.led - INVALID ARGUMENTS: channel = %d, percent = %.2lf" % (channel, percent))
