'''
Created on Jul 31, 2013

@author: mferreira
'''
import unittest
import sys
import re
from mock import patch
from cStringIO import StringIO

from seflabtools import loadmon
from seflabtools.exceptions import ArgumentsError
from seflabtools.loadmon import Monitor

class LoadmonPackageTest(unittest.TestCase):


    def setUp(self):
        self.old_stdout = sys.stdout
        sys.stdout = self.mystdout = StringIO()

    def tearDown(self):
        sys.out = self.old_stdout


    def testGetUsageInformation(self):
        usageInformation = loadmon.getUsageInformation("cmdName")

        self.assertIsNotNone(usageInformation)
        self.assertGreater(len(usageInformation), 0)


    def testParseArgumentsOnlyCommandName(self):
        argv = ["cmdName"]
        self.assertRaises(ArgumentsError, loadmon.parseArguments, argv)


    def testParseArgumentsDInvalidOption(self):
        argv = ["cmdName", "-x"]
        self.assertRaises(ArgumentsError, loadmon.parseArguments, argv)


    def testParseArgumentsDurationOptionButNoArgument(self):
        argv = ["cmdName", "-d"]
        self.assertRaises(ArgumentsError, loadmon.parseArguments, argv)


    def testParseArgumentsDurationExpandedOptionButNoArgument(self):
        argv = ["cmdName", "--duration"]
        self.assertRaises(ArgumentsError, loadmon.parseArguments, argv)


    def testParseArgumentsInvalidDuration(self):
        argv = ["cmdName", "-d", "not a number"]
        self.assertRaises(ArgumentsError, loadmon.parseArguments, argv)


    def testParseArgumentsDuration(self):
        argv = ["cmdName", "-d", "10"]
        duration = loadmon.parseArguments(argv)

        self.assertEqual(10, duration)


    def testMain(self):
        argv = ["cmdName", "-d", "1"]
        with patch.object(Monitor, 'start') as mockMonitorStart:
            loadmon.main(argv)

        mockMonitorStart.assert_called_with(1)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
