'''
Created on Jul 31, 2013

@author: mferreira
'''
from cStringIO import StringIO
from mock import patch
from seflabtools import synch
from seflabtools.exceptions import ArgumentsError
from seflabtools.synch.serialdevice import SerialDevice
from seflabtools.synch.synchronizer import Synchronizer
import os
import stat
import sys
import tempfile
import unittest
from seflabtools_tests.synch_tests import MockSerialDevice


class SynchPackageTest(unittest.TestCase):

    def setUp(self):
        self.old_stdout = sys.stdout
        sys.stdout = self.mystdout = StringIO()

    def tearDown(self):
        sys.out = self.old_stdout

    def testGetUsageInformation(self):
        usageInformation = synch.getUsageInformation("cmdName")

        self.assertIsNotNone(usageInformation)
        self.assertGreater(len(usageInformation), 0)

    def testParseArgumentsOnlyCommandName(self):
        argv = ["cmdName"]
        self.assertRaises(ArgumentsError, synch.parseArguments, argv)

    def testParseArgumentsDInvalidOption(self):
        argv = ["cmdName", "-x"]
        self.assertRaises(ArgumentsError, synch.parseArguments, argv)

    def testParseArgumentsDurationOptionButNoArgument(self):
        argv = ["cmdName", "-d"]
        self.assertRaises(ArgumentsError, synch.parseArguments, argv)

    def testParseArgumentsDurationExpandedOptionButNoArgument(self):
        argv = ["cmdName", "--duration"]
        self.assertRaises(ArgumentsError, synch.parseArguments, argv)

    def testParseArgumentsCommandOptionButNoArgument(self):
        argv = ["cmdName", "-c"]
        self.assertRaises(ArgumentsError, synch.parseArguments, argv)

    def testParseArgumentsCommandExpandedOptionButNoArgument(self):
        argv = ["cmdName", "--command"]
        self.assertRaises(ArgumentsError, synch.parseArguments, argv)

    def testParseArgumentsSerialOptionButNoArgument(self):
        argv = ["cmdName", "-s"]
        self.assertRaises(ArgumentsError, synch.parseArguments, argv)

    def testParseArgumentsSerialExpandedOptionButNoArgument(self):
        argv = ["cmdName", "--serial"]
        self.assertRaises(ArgumentsError, synch.parseArguments, argv)

    def testParseArgumentsOutputOptionButNoArgument(self):
        argv = ["cmdName", "-o"]
        self.assertRaises(ArgumentsError, synch.parseArguments, argv)

    def testParseArgumentsOutputExpandedOptionButNoArgument(self):
        argv = ["cmdName", "--output"]
        self.assertRaises(ArgumentsError, synch.parseArguments, argv)

    def testParseArgumentsModeOptionButNoArgument(self):
        argv = ["cmdName", "-m"]
        self.assertRaises(ArgumentsError, synch.parseArguments, argv)

    def testParseArgumentsModeExpandedOptionButNoArgument(self):
        argv = ["cmdName", "--mode"]
        self.assertRaises(ArgumentsError, synch.parseArguments, argv)

    def testParseArgumentsInvalidMode(self):
        argv = ["cmdName", "-m", "mode"]
        self.assertRaises(ArgumentsError, synch.parseArguments, argv)

    def testParseArgumentsModeRunWithoutCommand(self):
        argv = ["cmdName", "-s", "serial", "-m", "run"]
        self.assertRaises(ArgumentsError, synch.parseArguments, argv)

    def testParseArgumentsModeIdleWithoutDuration(self):
        argv = ["cmdName", "-s", "serial", "-m", "idle"]
        self.assertRaises(ArgumentsError, synch.parseArguments, argv)

    def testParseArgumentsModeIdleWithoutDurationZero(self):
        argv = ["cmdName", "-s", "serial", "-m", "idle", "-d", "0"]
        self.assertRaises(ArgumentsError, synch.parseArguments, argv)

    def testParseArgumentsModeIdleWithoutInvalidDuration(self):
        argv = ["cmdName", "-s", "serial", "-m", "idle", "-d", "string"]
        self.assertRaises(ArgumentsError, synch.parseArguments, argv)

    def testParseArgumentsOutputFileNotWritable(self):
        (_, tmpFile) = tempfile.mkstemp()
        os.chmod(tmpFile, stat.S_IREAD)
        argv = ["cmdName", "-s", "serial", "-m", "idle", "-d", "1", "-o", tmpFile]
        self.assertRaises(ArgumentsError, synch.parseArguments, argv)

    def testParseArgumentsModeIdle(self):
        argv = ["cmdName", "-s", "serial", "-m", "idle", "-d", "1"]
        (mode,
         serialPort,
         command,
         duration,
         outputFile) = synch.parseArguments(argv)

        self.assertEquals("idle", mode)
        self.assertEquals("serial", serialPort)
        self.assertIsNone(command)
        self.assertEquals(1, duration)
        self.assertIsNone(outputFile)

    def testParseArgumentsModeRun(self):
        (_, tmpFile) = tempfile.mkstemp()
        argv = ["cmdName", "-s", "serial", "-m", "run", "-d", "1", "-c", "command", "-o", tmpFile]
        (mode,
         serialPort,
         command,
         duration,
         outputFile) = synch.parseArguments(argv)

        self.assertEquals("run", mode)
        self.assertEquals("serial", serialPort)
        self.assertEquals("command", command)
        self.assertEquals(1, duration)
        self.assertEquals(tmpFile, outputFile)

    def testParseArgumentsModeRunWithouDuration(self):
        (_, tmpFile) = tempfile.mkstemp()
        argv = ["cmdName", "-s", "serial", "-m", "run", "-c", "command", "-o", tmpFile]
        (mode,
         serialPort,
         command,
         duration,
         outputFile) = synch.parseArguments(argv)

        self.assertEquals("run", mode)
        self.assertEquals("serial", serialPort)
        self.assertEquals("command", command)
        self.assertIsNone(duration)
        self.assertEquals(tmpFile, outputFile)

    @patch("seflabtools.synch.serialdevice.SerialDevice", spec=SerialDevice)
    @patch.object(SerialDevice, "init", new=lambda _: None)
    @patch.object(Synchronizer, "doIdle")
    def testMainIdle(self, mockSyncronizerDoIdle, _):
        argv = ["cmdName", "-s", "serial", "-m", "idle", "-d", "1"]
        synch.main(argv)

        mockSyncronizerDoIdle.assert_called_with(1)

    @patch("seflabtools.synch.serialdevice.SerialDevice", spec=SerialDevice)
    @patch.object(SerialDevice, "init", new=lambda _: None)
    @patch.object(SerialDevice, "setRTS", new=lambda _: None)
    @patch.object(Synchronizer, "doThreadedRun")
    def testMainRunWithDuration(self, mockSyncronizerDoRun, _):
        argv = ["cmdName", "-s", "serial", "-m", "run",
                "-d", "1", "-c", "command"]
        synch.main(argv)

        mockSyncronizerDoRun.assert_called_with("command", 1)

    @patch("seflabtools.synch.serialdevice.SerialDevice", spec=SerialDevice)
    @patch.object(SerialDevice, "init", new=lambda _: None)
    @patch.object(SerialDevice, "setRTS", new=lambda _: None)
    @patch.object(Synchronizer, "doRun")
    def testMainRunWithoutDuration(self, mockSyncronizerDoRun, _):
        argv = ["cmdName", "-s", "serial", "-m", "run", "-c", "command"]
        synch.main(argv)

        mockSyncronizerDoRun.assert_called_with("command")

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
