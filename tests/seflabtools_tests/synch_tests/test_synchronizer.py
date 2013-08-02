'''
SEFLab Tools is a software package that provides tools for running experiments in the SEFLab
as well as for analyzing the resulting data.

Copyright (C) 2013  Software Improvement Group

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
from cStringIO import StringIO
from datetime import datetime
from seflabtools.synch.synchronizer import Synchronizer
import multiprocessing
import psutil
import re
import sys
import tempfile
import time
import unittest


class SynchronizerTest(unittest.TestCase):

    def setUp(self):
        self.old_stdout = sys.stdout
        sys.stdout = self.mystdout = StringIO()
        self.serialPort = "test"

    def tearDown(self):
        sys.out = self.old_stdout

    def testDoSetup(self):
        synch = Synchronizer(self.serialPort, None)
        synch.doSetup()

        self.assertEqual(False, synch.serialDeviceWrapper.getRTS())
        self.assertEqual("RTS set to low... waiting 5 seconds\n", self.mystdout.getvalue())

    def testSendPulse(self):
        synch = Synchronizer(self.serialPort, None)
        synch.sendPulse(1)

        self.assertEqual([None, True], synch.serialDeviceWrapper.getRTSHistory())
        self.assertEqual(False, synch.serialDeviceWrapper.getRTS())

    def testRunCommand(self):
        synch = Synchronizer(self.serialPort, None)
        synch.runCommand("ls")

        self.assertEqual(None, synch.serialDeviceWrapper.getRTS())

    def testDoRunFunction(self):
        matcher = re.compile("RTS set to low... waiting 5 seconds\n" +
                             "Starting\n" +
                             "Function terminated.\n" +
                             "Start pulse sent at ' .* '; End Pulse sent at ' .* '\n")
        o = MockObjectWithFunction()
        synch = Synchronizer(self.serialPort, None)
        synch.doRunFunction(o.someFunction)

        self.assertEqual(1, o.getValue())
        self.assertIsNotNone(matcher.match(self.mystdout.getvalue()))
        self.assertEqual([None, False, True, False, True], synch.serialDeviceWrapper.getRTSHistory())
        self.assertEqual(False, synch.serialDeviceWrapper.getRTS())

    def testDoRun(self):
        matcher = re.compile("RTS set to low... waiting 5 seconds\n" +
                             "Starting\n" +
                             "Application terminated.\n" +
                             "Start pulse sent at ' .* '; End Pulse sent at ' .* '\n")
        synch = Synchronizer(self.serialPort, None)
        synch.doRun("ls")

        self.assertIsNotNone(matcher.match(self.mystdout.getvalue()))
        self.assertEqual([None, False, True, False, True], synch.serialDeviceWrapper.getRTSHistory())
        self.assertEqual(False, synch.serialDeviceWrapper.getRTS())

    def testTerminateProcessAndAllSubProcesses(self):
        synch = Synchronizer(self.serialPort, None)
        o = MockObjectWithFunction()
        process = multiprocessing.Process(target=o.spawnSomeSubProcessesAndDoNothing, args=[])
        process.start()
        synch.terminateProcessAndAllSubProcesses(process)

        proc = psutil.Process(process.pid)
        children = proc.get_children(recursive=True)

        self.assertIsNone(synch.serialDeviceWrapper.getRTS())
        self.assertEquals([], children)

    def testDoThreadedRun(self):
        matcher = re.compile("RTS set to low... waiting 5 seconds\n" +
                             "Starting\n" +
                             "Application terminated at timeout.\n" +
                             "Start pulse sent at ' .* '; End Pulse sent at ' .* '\n")
        synch = Synchronizer(self.serialPort, None)
        synch.doThreadedRun("sleep 10", 2)

        self.assertIsNotNone(matcher.match(self.mystdout.getvalue()))
        self.assertEqual([None, False, True, False, True], synch.serialDeviceWrapper.getRTSHistory())
        self.assertEqual(False, synch.serialDeviceWrapper.getRTS())

    def testDoIdle(self):
        matcher = re.compile("RTS set to low... waiting 5 seconds\n" +
                             "Starting\n" +
                             "Idle period terminated.\n" +
                             "Start pulse sent at ' .* '; End Pulse sent at ' .* '\n")
        synch = Synchronizer(self.serialPort, None)
        synch.doIdle(2)

        self.assertIsNotNone(matcher.match(self.mystdout.getvalue()))
        self.assertEqual([None, False, True, False, True], synch.serialDeviceWrapper.getRTSHistory())
        self.assertEqual(False, synch.serialDeviceWrapper.getRTS())

    def testPrintTimestampsNoFile(self):
        matcher = re.compile("Start pulse sent at ' 2013-07-31 09:14:00 '; End Pulse sent at ' 2013-07-31 10:14:00 '\n")
        synch = Synchronizer(self.serialPort, None)
        synch.printTimestamps(datetime(2013, 07, 31, 9, 14, 00), datetime(2013, 07, 31, 10, 14, 00), "test")

        self.assertIsNotNone(matcher.match(self.mystdout.getvalue()))
        self.assertIsNone(synch.serialDeviceWrapper.getRTS())

    def testPrintTimestampsWithFile(self):
        (_, outputFile) = tempfile.mkstemp()
        matcher = re.compile("Start pulse sent at ' 2013-07-31 09:14:00 '; End Pulse sent at ' 2013-07-31 10:14:00 '\n")
        synch = Synchronizer(self.serialPort, outputFile)
        synch.printTimestamps(datetime(2013, 07, 31, 9, 14, 00), datetime(2013, 07, 31, 10, 14, 00), "test")
        fin = open(outputFile, "r")
        lines = fin.readlines()

        self.assertIsNotNone(matcher.match(self.mystdout.getvalue()))
        self.assertEqual(1, len(lines))
        self.assertEquals(["2013-07-31 09:14:00, 2013-07-31 10:14:00, test\n"], lines)
        self.assertIsNone(synch.serialDeviceWrapper.getRTS())


class MockObjectWithFunction(object):
    def someFunction(self):
        self.value = self.value + 1

    def spawnSomeSubProcessesAndDoNothing(self):
        multiprocessing.Process(target=self.doNothing, args=[])
        multiprocessing.Process(target=self.doNothing, args=[])

    def doNothing(self):
        time.sleep(10)

    def getValue(self):
        return self.value

    def __init__(self):
        self.value = 0


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
