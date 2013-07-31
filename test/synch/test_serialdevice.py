'''
Created on Jul 31, 2013

@author: mferreira
'''
import unittest
from synch.serialdevice import AbstractSerialDevice

class AbstractSerialDeviceTest(unittest.TestCase):


    def testConstructor(self):
        deviceName = "device name"
        d = AbstractSerialDevice(deviceName)
        
        self.assertEqual(deviceName, d.deviceName)
    
    def testInit(self):
        deviceName = "device name"
        d = AbstractSerialDevice(deviceName)
        
        self.assertRaises(NotImplementedError, d.init)

    def testSetRTS(self):
        deviceName = "device name"
        d = AbstractSerialDevice(deviceName)
        
        self.assertRaises(NotImplementedError, d.setRTS, None)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()