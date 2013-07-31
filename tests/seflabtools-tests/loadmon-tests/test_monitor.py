'''
Created on Jul 31, 2013

@author: mferreira
'''
import unittest
import sys
import re
from cStringIO import StringIO

from seflabtools.loadmon import Monitor


class MonitorTest(unittest.TestCase):


    def setUp(self):
        self.old_stdout = sys.stdout
        sys.stdout = self.mystdout = StringIO()

    def tearDown(self):
        sys.out = self.old_stdout


    def testStart(self):
        matcher = re.compile("time, cpu, diskReadCount, diskWriteCount, diskReadBytes, diskWriteBytes\n" +
                             "([0-9]+([.][0-9]+)?, [0-9]+([.][0-9]+)?, [0-9]+([.][0-9]+)?, [0-9]+([.][0-9]+)?, [0-9]+([.][0-9]+)?, [0-9]+([.][0-9]+)?\n){5}")
        mon = Monitor()
        mon.start(5)

        self.assertIsNotNone(matcher.match(self.mystdout.getvalue()))




if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
