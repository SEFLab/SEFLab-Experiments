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
import sys
import serial
import time

from synchronizer import Synchronizer

RUN_MODE = "run"
IDLE_MODE = "idle"

def printUsage(cmdName):
    print "Usage: {0} -m <mode> -s <serial_port> [-c <command>] [-d <idle duration>] [-o <file>]".format(cmdName)
    print "-m\t\tsets the tool workign mode to run a command or idle for a period of time."
    print "  \t\tOptions are", RUN_MODE, "or", IDLE_MODE, "."
    print "  \t\tif duration is specified with mode run, then the tool will abort execution"
    print "  \t\tafter the defined number of seconds."
    print "-s\t\tselects through which serial port to send the synchronization pulse."
    print "-c\t\tdefines the command to execute."
    print "-d\t\tdefines the number of seconds the tool should idle for."
    print "-o\t\tdefines the file whereto print the timestamps to."

def parseArguments(argv):
    cmdName = os.path.basename(argv[0])
    try:
        opts, _ = getopt.getopt(argv[1:],"s:c:m:d:o:",["serial=", "command=", "mode=", "duration=", "output="])
    except getopt.GetoptError as e:
        print str(e)
        printUsage(cmdName)
        sys.exit(1)
    mode = None
    serial = None
    command = None
    durationString = None
    outputFile = None
    for opt, arg in opts:
        if opt in ("-m", "--mode"):
            mode = arg
        elif opt in ("-s", "--serial"):
            serial = arg
        elif opt in ("-c", "--command"):
            command = arg
        elif opt in ("-d", "--duration"):
            durationString = arg
        elif opt in ("-o", "--output"):
            outputFile = arg
    if serial == None:
        print "No serial port selected"
        printUsage(cmdName)
        sys.exit(2)
    if mode == RUN_MODE and command == None:
        print "Tool set to run command but no command was defined"
        printUsage(cmdName)
        sys.exit(3)
    if mode == IDLE_MODE and durationString == None:
        print "Tool set to idle but no duration was defined"
        printUsage(cmdName)
        sys.exit(4)
    if outputFile != None:
        try:
            file(outputFile, 'a').close()
        except IOError as e:
            print "Can't write to output file for timestamps. Reason: ", str(e)
            sys.exit(5)
    
    duration = 0
    if durationString != None:
        try:
            duration = float(durationString)
        except ValueError, e:
            print "Invalid duration:", str(e)
            printUsage(cmdName)
            sys.exit(6)
    
    return mode, serial, command, duration, outputFile
    
def main(argv):
    mode, serialPort, command, duration, outputFile = parseArguments(argv)
    
    synch = Synchronizer(serialPort, outputFile)
    
    if mode == RUN_MODE:
        if duration == None:
            synch.doRun(command)
        else:
            synch.doThreadedRun(command, duration)
    else:
        synch.doIdle(duration)

if __name__ == "__main__":
    main(sys.argv)
