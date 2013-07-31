'''
Created on Jul 31, 2013

@author: mferreira
'''
import unittest
import sys
from cStringIO import StringIO

import synch

class SynchPackageTest(unittest.TestCase):

    def setUp(self):
        self.old_stdout = sys.stdout
        sys.stdout = self.mystdout = StringIO()
        
    def tearDown(self):
        sys.out = self.old_stdout
        
    def testPrintUsage(self):
        synch.printUsage("cmd")
        output = self.mystdout.getvalue()
        
        self.assertIsNotNone(output)
        self.assertNotEqual("", output)
    
    def testParseArgumentsNoArguments(self):
        argv = ["cmdName"]
        synch.parseArguments(argv)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()