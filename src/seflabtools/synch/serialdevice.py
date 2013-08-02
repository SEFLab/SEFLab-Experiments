'''
Created on Jul 30, 2013

@author: mferreira
'''
import serial


def getSerialDeviceWrapper(serialPort):
    device = None
    if serialPort == "test":
        device = MockSerialDevice(serialPort)
    else:
        device = SerialDevice(serialPort)

    device.init()
    return device


class AbstractSerialDevice(object):
    '''
    classdocs
    '''
    def init(self):
        raise NotImplementedError("This method is of an abstract class")

    def setRTS(self, level):
        raise NotImplementedError("This method is of an abstract class")

    def __init__(self, serialPort):
        '''
        Constructor
        '''
        self.serialPort = serialPort


class SerialDevice(AbstractSerialDevice):
    def init(self):
        self.serial = serial.Serial(self.serialPort)

    def setRTS(self, level):
        self.serial.setRTS(level)


class MockSerialDevice(AbstractSerialDevice):

    def init(self):
        self.statusRTS = None
        self.statusRTSHistory = []

    def setRTS(self, level):
        self.statusRTSHistory.append(self.statusRTS)
        self.statusRTS = level

    def getRTS(self):
        return self.statusRTS

    def getRTSHistory(self):
        return self.statusRTSHistory

    def clearRTSHistory(self):
        self.statusRTSHistory = []
