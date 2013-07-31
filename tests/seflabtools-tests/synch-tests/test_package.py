'''
Created on Jul 31, 2013

@author: mferreira
'''
import unittest
import sys
from cStringIO import StringIO

from seflabtools.exceptions import ArgumentsError
from seflabtools import synch

class SynchPackageTest(unittest.TestCase):

    def setUp(self):
        self.old_stdout = sys.stdout
        sys.stdout = self.mystdout = StringIO()
        
    def tearDown(self):
        sys.out = self.old_stdout
        
    def testGetUsageInformation(self):
        usageInformation = synch.getUsageInformation("cmd")
        
        self.assertIsNotNone(usageInformation)
        self.assertGreater(len(usageInformation), 0)
    
    def testParseArgumentsNoArguments(self):
        argv = ["cmdName"]
        
        self.assertRaises(ArgumentsError, synch.parseArguments, argv)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()