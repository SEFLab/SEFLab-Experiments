'''
Created on Jul 31, 2013

@author: mferreira
'''
import unittest
import sys
from mock import patch
from cStringIO import StringIO

import seflabtools
from seflabtools import synch
from seflabtools import loadgen
from seflabtools import loadmon
from seflabtools.exceptions import ArgumentsError

class SeflabToolsPackageTest(unittest.TestCase):


    def setUp(self):
        self.old_stdout = sys.stdout
        sys.stdout = self.mystdout = StringIO()


    def tearDown(self):
        sys.out = self.old_stdout


    def testGetToolOptions(self):
        toolOptions = seflabtools.getToolOptions(["a", "b"])

        self.assertEquals(["a", "|", "b"], toolOptions)


    def testGetUsageInformation(self):
        usageInformation = seflabtools.getUsageInformation("cmdName", ["a", "b"])

        self.assertIsNotNone(usageInformation)
        self.assertGreater(len(usageInformation), 0)


    def testParseArgumentsOnlyCommandName(self):
        argv = ["cmdName"]
        self.assertRaises(ArgumentsError, seflabtools.parseArguments, argv)


    def testParseArgumentsHelp(self):
        argv = ["cmdName", "-h"]
        tool = seflabtools.parseArguments(argv)

        self.assertEqual("help", tool)


    def testParseArgumentsToolOptionButNoArgument(self):
        argv = ["cmdName", "-t"]
        self.assertRaises(ArgumentsError, seflabtools.parseArguments, argv)


    def testParseArgumentsToolOptionWithInvalidTool(self):
        argv = ["cmdName", "-t", "notool"]
        self.assertRaises(ArgumentsError, seflabtools.parseArguments, argv)


    def testParseArgumentsSynchTool(self):
        toolName = "synch"
        argv = ["cmdName", "-t", toolName]
        tool = seflabtools.parseArguments(argv)

        self.assertEqual(toolName, tool)


    def testParseArgumentsLoadmonTool(self):
        toolName = "loadmon"
        argv = ["cmdName", "-t", toolName]
        tool = seflabtools.parseArguments(argv)

        self.assertEqual(toolName, tool)


    def testParseArgumentsLoadgenTool(self):
        toolName = "loadgen"
        argv = ["cmdName", "-t", toolName]
        tool = seflabtools.parseArguments(argv)

        self.assertEqual(toolName, tool)


    def testMainHelp(self):
        argv = ["cmdName", "-h"]
        seflabtools.main(argv)
        output = self.mystdout.getvalue()

        self.assertIsNotNone(output)
        self.assertEquals(output, seflabtools.getUsageInformation("cmdName", seflabtools.availableTools) + "\n")


    def testMainSynchTool(self):
        toolName = "synch"
        argv = ["cmdName", "-t", toolName]
        with patch.object(synch, 'main') as mock:
            seflabtools.main(argv)

        mock.assert_called_with(argv[2:])


    def testMainLoadgenTool(self):
        toolName = "loadgen"
        argv = ["cmdName", "-t", toolName]
        with patch.object(loadgen, 'main') as mock:
            seflabtools.main(argv)

        mock.assert_called_with(argv[2:])


    def testMainSynchTool(self):
        toolName = "loadmon"
        argv = ["cmdName", "-t", toolName]
        with patch.object(loadmon, 'main') as mock:
            seflabtools.main(argv)

        mock.assert_called_with(argv[2:])


    def testMainNoOptions(self):
        argv = ["cmdName"]
        seflabtools.main(argv)
        output = self.mystdout.getvalue()

        self.assertIsNotNone(output)
        self.assertGreater(len(output), 0)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
