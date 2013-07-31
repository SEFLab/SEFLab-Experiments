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
import unittest

from seflabtools.loadgen import Controller
from seflabtools.loadgen import CPUWorker
from seflabtools.loadgen import HDDWorker

class ControllerTest(unittest.TestCase):


    def testStartCPU(self):
        ctr = Controller(10, CPUWorker(True))
        ctr.start()

    def testStartHDD(self):
        ctr = Controller(10, HDDWorker(False))
        ctr.start()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testStart']
    unittest.main()