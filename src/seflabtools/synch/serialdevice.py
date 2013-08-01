'''
Created on Jul 30, 2013

@author: mferreira
'''
import serial


class AbstractSerialDevice(object):
    '''
    classdocs
    '''
    def init(self):
        raise NotImplementedError("This method is of an abstract class")

    def setRTS(self, level):
        raise NotImplementedError("This method is of an abstract class")

    def __init__(self, deviceName):
        '''
        Constructor
        '''
        self.deviceName = deviceName


class SerialDevice(AbstractSerialDevice):
    def init(self):
        self.serial = serial.Serial(self.deviceName)

    def setRTS(self, level):
        self.serial.setRTS(level)
