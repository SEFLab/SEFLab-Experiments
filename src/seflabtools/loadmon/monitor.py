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

import psutil
import time


class Monitor(object):

    def start(self, duration):
        loopCondition = True
        ioStats = psutil.disk_io_counters()
        readCount = ioStats.read_count
        writeCount = ioStats.write_count
        readBytes = ioStats.read_bytes
        writeBytes = ioStats.write_bytes
        print "time, cpu, diskReadCount, diskWriteCount, diskReadBytes, diskWriteBytes"
        start = time.time()
        while loopCondition:
            ioStats = psutil.disk_io_counters()
            print "{0}, {1}, {2}, {3}, {4}, {5}".format(time.time(),
                                       str(psutil.cpu_percent(interval=1)),
                                       ioStats.read_count - readCount,
                                       ioStats.write_count - writeCount,
                                       ioStats.read_bytes - readBytes,
                                       ioStats.write_bytes - writeBytes)
            readCount = ioStats.read_count
            writeCount = ioStats.write_count
            readBytes = ioStats.read_bytes
            writeBytes = ioStats.write_bytes
            if duration > 0:
                loopCondition = start + duration > time.time()

    def __init__(self):
        '''
        Constructor
        '''
