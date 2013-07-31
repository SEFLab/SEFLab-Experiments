'''
Created on Jul 31, 2013

@author: mferreira
'''
from cStringIO import StringIO
from seflabtools import loadgen
from seflabtools.exceptions import ArgumentsError
from seflabtools.loadgen.worker import CPUWorker, HDDWorker
import os
import re
import stat
import sys
import tempfile
import unittest


class LoadgenPackageTest(unittest.TestCase):


    def setUp(self):
        self.old_stdout = sys.stdout
        sys.stdout = self.mystdout = StringIO()

    def tearDown(self):
        sys.out = self.old_stdout


    def testGetUsageInformation(self):
        usageInformation = loadgen.getUsageInformation("cmdName")

        self.assertIsNotNone(usageInformation)
        self.assertGreater(len(usageInformation), 0)


    def testParseArgumentsOnlyCommandName(self):
        argv = ["cmdName"]
        self.assertRaises(ArgumentsError, loadgen.parseArguments, argv)


    def testParseArgumentsDInvalidOption(self):
        argv = ["cmdName", "-x"]
        self.assertRaises(ArgumentsError, loadgen.parseArguments, argv)


    def testParseArgumentsDurationOptionButNoArgument(self):
        argv = ["cmdName", "-d"]
        self.assertRaises(ArgumentsError, loadgen.parseArguments, argv)


    def testParseArgumentsDurationExpandedOptionButNoArgument(self):
        argv = ["cmdName", "--duration"]
        self.assertRaises(ArgumentsError, loadgen.parseArguments, argv)


    def testParseArgumentsWorkerOptionButNoArgument(self):
        argv = ["cmdName", "-w"]
        self.assertRaises(ArgumentsError, loadgen.parseArguments, argv)


    def testParseArgumentsWorkerExpandedOptionButNoArgument(self):
        argv = ["cmdName", "--worker"]
        self.assertRaises(ArgumentsError, loadgen.parseArguments, argv)


    def testParseArgumentsSerialOptionButNoArgument(self):
        argv = ["cmdName", "-s"]
        self.assertRaises(ArgumentsError, loadgen.parseArguments, argv)


    def testParseArgumentsSerialExpandedOptionButNoArgument(self):
        argv = ["cmdName", "--serial"]
        self.assertRaises(ArgumentsError, loadgen.parseArguments, argv)


    def testParseArgumentsOutputOptionButNoArgument(self):
        argv = ["cmdName", "-s"]
        self.assertRaises(ArgumentsError, loadgen.parseArguments, argv)


    def testParseArgumentsOutputExpandedOptionButNoArgument(self):
        argv = ["cmdName", "--serial"]
        self.assertRaises(ArgumentsError, loadgen.parseArguments, argv)


    def testParseArgumentsInvalidWorker(self):
        argv = ["cmdName", "-w", "worker"]
        self.assertRaises(ArgumentsError, loadgen.parseArguments, argv)


    def testParseArgumentsDurationIsZero(self):
        argv = ["cmdName", "-d", "0"]
        self.assertRaises(ArgumentsError, loadgen.parseArguments, argv)


    def testParseArgumentsDurationIsString(self):
        argv = ["cmdName", "-w", "cpu", "-d", "string"]
        self.assertRaises(ArgumentsError, loadgen.parseArguments, argv)


    def testParseArgumentsOutputFileNotWritable(self):
        (_, tmpFile) = tempfile.mkstemp()
        os.chmod(tmpFile, stat.S_IREAD)
        argv = ["cmdName", "-w", "cpu", "-d", "1", "-o", tmpFile]
        self.assertRaises(ArgumentsError, loadgen.parseArguments, argv)


    def testParseArguments(self):
        argv = ["cmdName", "-w", "cpu", "-d", "1"]
        (worker,
         duration,
         serialPort,
         outputFile) = loadgen.parseArguments(argv)

        self.assertIsInstance(worker, CPUWorker)
        self.assertEquals(1, duration)
        self.assertIsNone(serialPort)
        self.assertIsNone(outputFile)


    def testParseArgumentsWithSerialAndOutputFile(self):
        serialDevice = "serial"
        (_, tmpFile) = tempfile.mkstemp()
        argv = ["cmdName", "-w", "hdd", "-d", "1", "-s", serialDevice, "-o", tmpFile]
        (worker,
         duration,
         serialPort,
         outputFile) = loadgen.parseArguments(argv)

        self.assertIsInstance(worker, HDDWorker)
        self.assertEquals(1, duration)
        self.assertEquals(serialDevice, serialPort)
        self.assertEquals(tmpFile, outputFile)



if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
