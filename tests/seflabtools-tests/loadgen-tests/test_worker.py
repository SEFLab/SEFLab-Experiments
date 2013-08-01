'''
Created on Aug 1, 2013

@author: mferreira
'''
from mock import Mock, patch
from seflabtools.loadgen.worker import Worker, CPUWorker, HDDWorker
from tempfile import SpooledTemporaryFile
import multiprocessing
import random
import time
import unittest


class WorkerTest(unittest.TestCase):

    @patch("seflabtools.loadgen.worker.Worker", spec=Worker)
    def testDoWork(self, mockWorker):
        self.assertRaises(NotImplementedError, Worker.doWork, mockWorker)

    @patch.object(Worker, "__init__", new=lambda x: None)
    @patch.object(random, "randrange", new=lambda x, y: 3)
    @patch.object(multiprocessing.Process, "join")
    @patch.object(multiprocessing.Process, "start")
    def testStartWorkers(self, mockProcessStart, mockProcessJoin):
        worker = Worker()
        worker.startWorkers()

        self.assertEqual(2, mockProcessStart.call_count)
        self.assertEqual(2, mockProcessJoin.call_count)

    @patch.object(Worker, "__init__", new=lambda x: None)
    @patch.object(Worker, "doWork")
    def testStart(self, mockWorkerDoWork):
        duration = 1
        worker = Worker()
        worker.multiworker = False
        worker.start(duration)

        self.assertEquals(duration, worker.duration)


class CPUWorkerTest(unittest.TestCase):

    @patch.object(time, "time", new=lambda : 3)
    @patch.object(random, "seed")
    def testConstructor(self, mockRandomSeed):
        multiworker = False
        cpuWorker = CPUWorker(multiworker)

        self.assertEquals(multiworker, cpuWorker.multiworker)
        mockRandomSeed.assert_called_with(3)


class HDDWorkerTest(unittest.TestCase):


    @patch.object(time, "time", new=lambda : 3)
    @patch.object(random, "seed")
    def testConstructor(self, mockRandomSeed):
        multiworker = True
        hddWorker = HDDWorker(multiworker)

        self.assertEquals(multiworker, hddWorker.multiworker)
        mockRandomSeed.assert_called_with(3)

    @patch.object(random, "randrange", new=lambda x, y: 1)
    @patch.object(time, "sleep")
    @patch.object(SpooledTemporaryFile, "read")
    @patch.object(SpooledTemporaryFile, "write")
    def testDoWorkWrite(self, mockWrite, mockRead, mockTimeSleep):
        multiworker = False
        hddWorker = HDDWorker(multiworker)
        hddWorker.duration = 1
        hddWorker.doWork()

        mockWrite.assert_called()
        self.assertEquals(0, mockRead.call_count)
        self.assertEquals(0, mockTimeSleep.call_count)

    @patch.object(random, "randrange", new=lambda x, y: 2)
    @patch.object(time, "sleep")
    @patch.object(SpooledTemporaryFile, "read")
    @patch.object(SpooledTemporaryFile, "write")
    def testDoWorkWrite(self, mockWrite, mockRead, mockTimeSleep):
        multiworker = False
        hddWorker = HDDWorker(multiworker)
        hddWorker.duration = 1
        hddWorker.doWork()

        mockRead.assert_called()
        self.assertEquals(0, mockWrite.call_count)
        self.assertEquals(0, mockTimeSleep.call_count)

    @patch.object(random, "randrange", new=lambda x, y: 3)
    @patch.object(time, "sleep")
    @patch.object(SpooledTemporaryFile, "read")
    @patch.object(SpooledTemporaryFile, "write")
    def testDoWorkWrite(self, mockWrite, mockRead, mockTimeSleep):
        multiworker = False
        hddWorker = HDDWorker(multiworker)
        hddWorker.duration = 1
        hddWorker.doWork()

        mockTimeSleep.assert_called()
        self.assertEquals(0, mockWrite.call_count)
        self.assertEquals(0, mockRead.call_count)




if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
