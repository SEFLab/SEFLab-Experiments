'''
Created on Aug 1, 2013

@author: mferreira
'''
import unittest
import random
import time
from mock import patch
from seflabtools.loadgen.worker import CPUWorker
from seflabtools.loadgen.controller import Controller

class ControllerTest(unittest.TestCase):

    def testConstructor(self):
        t = 10
        duration = 1
        worker = CPUWorker(False)
        with patch.object(random, "seed") as mockRandomSeed:
            with patch.object(time, "time") as mockTimeTime:
                mockTimeTime.return_value = t
                c = Controller(duration, worker)

        self.assertEqual(duration, c.duration)
        self.assertEquals(worker, c.worker)
        mockRandomSeed.assert_called_with(t)

    def testStart(self):
        randValue = 5
        duration = 3
        duration = 1
        worker = CPUWorker(False)
        c = Controller(duration, worker)
        with patch.object(random, "randrange") as mockRandomRandrange:
            mockRandomRandrange.return_value = 5
            with patch.object(CPUWorker, "start") as mockCPUWorkerStart:
                 c.start()

        mockRandomRandrange.assert_called_with(1, 2)
        mockCPUWorkerStart.assert_called_with(randValue)



if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
