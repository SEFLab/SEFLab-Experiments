'''
Created on Jul 30, 2013

@author: mferreira
'''
import unittest
import sys
import re
import multiprocessing
import time
import psutil
from cStringIO import StringIO

from synch.synchronizer import Synchronizer
from synch.serialdevice import AbstractSerialDevice

class SynchronizerTest(unittest.TestCase):


    def setUp(self):
        self.old_stdout = sys.stdout
        sys.stdout = self.mystdout = StringIO()
        self.serialDeviceWrapper = MockSerialDevice("mockdevice")
        self.serialDeviceWrapper.init()

    def tearDown(self):
        sys.out = self.old_stdout
        pass


    def testDoSetup(self):
        self.serialDeviceWrapper.setRTS(True)
        synch = Synchronizer(None, self.serialDeviceWrapper)
        synch.doSetup()
        
        self.assertEqual(False, self.serialDeviceWrapper.getRTS())
        self.assertEqual("RTS set to low... waiting 5 seconds\n", self.mystdout.getvalue())

    def testSendPulse(self):
        synch = Synchronizer(None, self.serialDeviceWrapper)
        synch.sendPulse(1)
        
        self.assertEqual([None, True], self.serialDeviceWrapper.getRTSHistory())
        self.assertEqual(False, self.serialDeviceWrapper.getRTS())

    def testRunCommand(self):
        synch = Synchronizer(None, self.serialDeviceWrapper)
        synch.runCommand("ls")
        
        self.assertEqual(None, self.serialDeviceWrapper.getRTS())

    def testDoRunFunction(self):
        matcher = re.compile("RTS set to low... waiting 5 seconds\n" +
                             "Starting\n" +
                             "Function terminated.\n" +
                             "Start pulse sent at ' .* '; End Pulse sent at ' .* '\n")
        o = MockObjectWithFunction()
        synch = Synchronizer(None, self.serialDeviceWrapper)
        synch.doRunFunction(o.someFunction)
        
        self.assertEqual(1, o.getValue())
        self.assertIsNotNone(matcher.match(self.mystdout.getvalue()))
        self.assertEqual([None, False, True, False, True], self.serialDeviceWrapper.getRTSHistory())
        self.assertEqual(False, self.serialDeviceWrapper.getRTS())
    
    def testDoRun(self):
        matcher = re.compile("RTS set to low... waiting 5 seconds\n" +
                             "Starting\n" +
                             "Application terminated.\n" +
                             "Start pulse sent at ' .* '; End Pulse sent at ' .* '\n")
        synch = Synchronizer(None, self.serialDeviceWrapper)
        synch.doRun("ls")
        
        self.assertIsNotNone(matcher.match(self.mystdout.getvalue()))
        self.assertEqual([None, False, True, False, True], self.serialDeviceWrapper.getRTSHistory())
        self.assertEqual(False, self.serialDeviceWrapper.getRTS())
    
    def testTerminateProcessAndAllSubProcesses(self):
        synch = Synchronizer(None, self.serialDeviceWrapper)
        o = MockObjectWithFunction()
        process = multiprocessing.Process(target = o.spawnSomeSubProcessesAndDoNothing, args = [])
        process.start()
        synch.terminateProcessAndAllSubProcesses(process)
        
        proc = psutil.Process(process.pid)
        children = proc.get_children(recursive=True)
        
        self.assertIsNone(self.serialDeviceWrapper.getRTS())
        self.assertEquals([], children)

class MockSerialDevice(AbstractSerialDevice):
    def init(self):
        self.statusRTS = None;
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

class MockObjectWithFunction(object):
    def someFunction(self):
        self.value = self.value + 1
    
    def spawnSomeSubProcessesAndDoNothing(self):
        multiprocessing.Process(target = self.doNothing, args = [])
        multiprocessing.Process(target = self.doNothing, args = [])
    
    def doNothing(self):
        time.sleep(10)
    
    def getValue(self):
        return self.value
    
    def __init__(self):
        self.value = 0
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()