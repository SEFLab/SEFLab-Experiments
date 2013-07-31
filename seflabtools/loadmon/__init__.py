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
import getopt
import os
import time
import psutil
import sys

from seflabtools.exceptions import ArgumentsError  # @UnresolvedImport
from monitor import Monitor

def getUsageInformation(cmdName):
    usageInformation = "" 
    usageInformation += "Usage: {0} -d <duration_in_seconds> ...\n".format(cmdName)
    usageInformation += "-d\t\tdefines for how long (in seconds) load should be monitored\n"
    usageInformation += "  \t\tif duration is <= 0 then load will be monitored continuously\n"
    return usageInformation

def parseArguments(argv):
    cmdName = os.path.basename(argv[0])
    usageInformation = getUsageInformation(cmdName)
    durationString = ''
    try:
        opts, _ = getopt.getopt(argv[1:],"d:",["duration="])
    except getopt.GetoptError as e:
        raise ArgumentsError(str(e), usageInformation)
    for opt, arg in opts:
        if opt in ("-d", "--duration"):
            durationString = arg
    if durationString == '':
        raise ArgumentsError("Need a duration value. If you want to monitor continuously set a duration <= 0", usageInformation)
    duration = 0
    try:
        duration = float(durationString)
    except ValueError, e:
        raise ArgumentsError("Invalid duration: " + str(e), usageInformation)
    
    return duration

def main(argv):
    duration = parseArguments(argv)
    monitor = Monitor()
    monitor.start(duration)
