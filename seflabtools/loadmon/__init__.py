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


def printUsage(cmdName):
    print "Usage: {0} -d <duration_in_seconds> ...".format(cmdName)
    print "-d\t\tdefines for how long (in seconds) load should be monitored"
    print "  \t\tif duration is <= 0 then load will be monitored continuously"
    
def parseArguments(argv):
    cmdName = os.path.basename(argv[0])
    durationString = ''
    try:
        opts, _ = getopt.getopt(argv[1:],"d:",["duration="])
    except getopt.GetoptError:
        printUsage(cmdName)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-d", "--duration"):
            durationString = arg
    if durationString == '':
        print "Need a duration value. If you want to monitor continuously set a duration <= 0"
        printUsage(cmdName)
        sys.exit(3)
    duration = 0
    try:
        duration = float(durationString)
    except ValueError, e:
        print "Invalid duration:", str(e)
        printUsage(cmdName)
        sys.exit(4)
    
    return duration

def main(argv):
    duration = parseArguments(argv)
    monitor = Monitor()
    monitor.start(duration)

if __name__ == "__main__":
    import getopt
    import os
    import time
    import psutil
    import sys
    
    from monitor import Monitor

    main(sys.argv)